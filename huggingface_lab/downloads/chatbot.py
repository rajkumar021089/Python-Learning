"""AI Engineering Stage 3: Qwen chatbot with SQLite + context window + summary.

Features:
  * The full conversation stays in chatbot_memory.db.
  * Recent exchanges are sent within a token budget.
  * A short LLM-generated summary of older exchanges is saved in SQLite.
  * /memory shows the saved summary; /compact processes an additional 3 batches.

The summary is approximate and may omit details. Never treat it as an exact record.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "downloads" / "model" / "qwen-mini"
DB_PATH = BASE_DIR / "chatbot_memory.db"

SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and concisely."
MAX_RECENT_MESSAGES = 20        # Up to ten recent user/assistant pairs
MAX_INPUT_TOKENS = 1800         # Input budget, set for practice
MAX_NEW_TOKENS = 200            # Chat response budget
SUMMARY_BATCH_SIZE = 8         # Compress four old user/assistant pairs per batch
SUMMARY_INPUT_TOKENS = 1100     # Smaller budget for the summary operation
SUMMARY_NEW_TOKENS = 160       # Upper bound for new summary text


def initialize_database():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_summary (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    content TEXT NOT NULL,
                    last_message_id INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                INSERT OR IGNORE INTO memory_summary (id, content, last_message_id)
                VALUES (1, '', 0)
            """)


def load_recent_rows(limit=MAX_RECENT_MESSAGES):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute(
            "SELECT id, role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return list(reversed(rows))


def load_summary():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        row = conn.execute(
            "SELECT content, last_message_id FROM memory_summary WHERE id = 1"
        ).fetchone()
    return (row[0], row[1]) if row else ("", 0)


def save_exchange(user_text, assistant_text):
    """Commit the whole pair atomically, keeping history in valid order."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.executemany(
                "INSERT INTO conversations (role, content) VALUES (?, ?)",
                [("user", user_text), ("assistant", assistant_text)],
            )


def make_prompt_messages(history, question, summary):
    system_text = SYSTEM_PROMPT
    if summary:
        system_text += (
            "\n\nSummary of older conversation (may omit details; prefer recent messages "
            "when they conflict):\n" + summary
        )
    return [
        {"role": "system", "content": system_text},
        *history,
        {"role": "user", "content": question},
    ]


def tokenized_prompt(tokenizer, messages):
    return tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )


def generate_text(model, tokenizer, inputs, max_new_tokens):
    inputs = inputs.to(model.device)
    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated_only = generated_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated_only, skip_special_tokens=True).strip()


def summarize_one_batch(model, tokenizer):
    """Compress up to 8 *older* stored messages; do not touch recent 20.

    Returns True if a summary was durably updated. False means no batch is ready.
    This never loads the full conversation into Python.
    """
    recent = load_recent_rows()
    if len(recent) < MAX_RECENT_MESSAGES:
        return False

    oldest_recent_id = recent[0][0]
    previous_summary, last_id = load_summary()

    with closing(sqlite3.connect(DB_PATH)) as conn:
        old_rows = conn.execute(
            """SELECT id, role, content FROM conversations
               WHERE id > ? AND id < ? ORDER BY id LIMIT ?""",
            (last_id, oldest_recent_id, SUMMARY_BATCH_SIZE),
        ).fetchall()

    # Summarize complete pairs in batches. Avoid one additional model call
    # for every chat turn; run once for each four expired exchanges.
    if len(old_rows) < SUMMARY_BATCH_SIZE:
        return False
    roles = [row[1] for row in old_rows]
    if roles != ["user", "assistant"] * (SUMMARY_BATCH_SIZE // 2):
        raise ValueError("Old conversation records are not complete user/assistant pairs.")

    summary_instructions = (
        "Summarize the earlier conversation for future reference. "
        "Keep only facts the USER explicitly provided, user preferences, decisions, "
        "and ongoing tasks. Never invent details. Maintain useful details from "
        "the previous summary. Be concise (ideally under 110 words). "
        "Return ONLY the updated summary as plain text."
    )

    # Limit input size even if an old chat message contains a huge pasted file.
    # Truncation makes this an approximate summary, not a replacement for raw SQLite data.
    excerpt_chars = 350
    while True:
        conversation_excerpt = "\n".join(
            f"{role}: {content[:excerpt_chars]}"
            for _, role, content in old_rows
        )
        summary_user_message = (
            f"Previous summary:\n{previous_summary[:1200] or '(none)'}\n\n"
            f"Older exchanges to absorb:\n{conversation_excerpt}"
        )
        inputs = tokenized_prompt(tokenizer, [
            {"role": "system", "content": summary_instructions},
            {"role": "user", "content": summary_user_message},
        ])
        if inputs["input_ids"].shape[1] <= SUMMARY_INPUT_TOKENS:
            break
        if excerpt_chars <= 60:
            raise ValueError("Summary input exceeds its token budget.")
        excerpt_chars //= 2

    new_summary = generate_text(model, tokenizer, inputs, SUMMARY_NEW_TOKENS)
    if not new_summary:
        raise ValueError("The model returned an empty summary; history was not advanced.")

    # Save the summary and checkpoint together. Original messages remain intact.
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            updated = conn.execute(
                """UPDATE memory_summary
                   SET content = ?, last_message_id = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = 1 AND last_message_id = ?""",
                (new_summary, old_rows[-1][0], last_id),
            )
            if updated.rowcount != 1:
                raise RuntimeError("Summary checkpoint changed; retry safely.")
    print(f"[Memory: summarized {len(old_rows)//2} old exchanges into SQLite]")
    return True


def build_limited_context(tokenizer, user_input):
    rows = load_recent_rows()
    history = [{"role": role, "content": content} for _, role, content in rows]
    summary, _ = load_summary()
    trimmed_exchanges = 0

    while True:
        messages = make_prompt_messages(history, user_input, summary)
        inputs = tokenized_prompt(tokenizer, messages)
        tokens = inputs["input_ids"].shape[1]
        if tokens <= MAX_INPUT_TOKENS:
            return inputs, len(history) // 2, trimmed_exchanges, bool(summary)
        if not history:
            raise ValueError(
                f"System prompt + memory summary + question need {tokens} tokens "
                f"(limit {MAX_INPUT_TOKENS}). Shorten the question."
            )
        if len(history) < 2 or [history[0]["role"], history[1]["role"]] != ["user", "assistant"]:
            raise ValueError("Recent history is not in complete user/assistant pairs.")
        del history[:2]
        trimmed_exchanges += 1


def main():
    initialize_database()
    if not MODEL_DIR.is_dir():
        raise FileNotFoundError(
            f"Model not found at {MODEL_DIR}\n"
            "Set MODEL_DIR to the location of your downloaded Qwen model."
        )

    print(f"Loading local Qwen model: {MODEL_DIR}")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(str(MODEL_DIR), local_files_only=True)
    model.eval()
    print(f"SQLite DB: {DB_PATH}")
    print("Commands: /memory (show summary), /compact (process up to 3 batches), exit\n")

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        if question.lower() == "/memory":
            summary, last_id = load_summary()
            print(f"[Saved summary through message id {last_id}]\n{summary or '(empty)'}\n")
            continue
        if question.lower() == "/compact":
            try:
                processed = sum(summarize_one_batch(model, tokenizer) for _ in range(3))
                print(f"[Compacted batches: {processed}]\n")
            except Exception as exc:
                print(f"Could not summarize: {exc}\n")
            continue

        try:
            summarize_one_batch(model, tokenizer)  # At most one batch per chat turn.
        except Exception as exc:
            # Summarization failure should not prevent ordinary chat.
            print(f"[Memory summary warning: {exc}]")

        try:
            inputs, kept_pairs, trimmed_pairs, has_summary = build_limited_context(tokenizer, question)
        except ValueError as exc:
            print(f"Context warning: {exc}\n")
            continue

        count = inputs["input_ids"].shape[1]
        print(
            f"[Context: {count}/{MAX_INPUT_TOKENS} input tokens; "
            f"{kept_pairs} recent exchanges; {trimmed_pairs} trimmed; "
            f"saved summary: {'yes' if has_summary else 'no'}]"
        )

        try:
            answer = generate_text(model, tokenizer, inputs, MAX_NEW_TOKENS)
        except Exception as exc:
            print(f"Generation failed: {exc}\n")
            continue
        if not answer:
            print("Model produced no answer; nothing saved.\n")
            continue

        print(f"AI: {answer}\n")
        try:
            save_exchange(question, answer)
        except sqlite3.Error as exc:
            print(f"Database warning: answer was not saved: {exc}\n")


if __name__ == "__main__":
    main()
