import json
from contextlib import closing
from ollama import chat

MODEL="mistral:latest"

def run_agent(question: str):
    response = chat(
        model=MODEL,
        format="json",
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI Assistant.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return json.loads(response.message.content)["content"]

if __name__ == "__main__":
    while True:
        question=input("\nYou:").strip()

        if question.lower in ('exit','quit'):
            break

        if not question:
            continue

        try:
            answer = run_agent(question)
            print("\nAI:", answer)

        except Exception as error:
            print("Agent execution failed:", error)
