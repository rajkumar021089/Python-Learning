from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "./model/qwen-mini",
    local_files_only=True
)

text = "AI IS AN EMOTION"

tokens = tokenizer.tokenize(text)

token_ids = tokenizer.encode(
    text,
    add_special_tokens=False
)

print("Original:", text)
print("Tokens:", tokens)
print("Token IDs:", token_ids)
print("Total Tokens:", len(token_ids))