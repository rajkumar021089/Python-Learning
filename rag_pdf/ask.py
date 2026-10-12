import requests
import chromadb


# --------------------------------
# 1. CONNECT TO CHROMA DB
# --------------------------------

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="intellistay_docs",
    embedding_function=None
)


# --------------------------------
# 2. GET USER QUESTION
# --------------------------------

question = input("Ask a question: ")


# --------------------------------
# 3. CREATE QUESTION EMBEDDING
# --------------------------------

embed_url = "http://localhost:11434/api/embed"

embed_payload = {
    "model": "nomic-embed-text",
    "input": question
}

response = requests.post(
    embed_url,
    json=embed_payload
)

question_embedding = response.json()["embeddings"][0]


# --------------------------------
# 4. RETRIEVE FROM CHROMA DB
# --------------------------------

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

retrieved_chunks = results["documents"][0]


# --------------------------------
# 5. COMBINE RETRIEVED CHUNKS
# --------------------------------

context = "\n\n".join(retrieved_chunks)


print("\nRetrieved Context:")
print("==============================")
print(context)


# --------------------------------
# 6. CREATE PROMPT FOR LLM
# --------------------------------

prompt = f"""
You are an assistant answering questions about IntelliStay HMS.

Answer the question using ONLY the context provided below.

If the answer cannot be found in the context,
say "I could not find this information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""


# --------------------------------
# 7. CALL QWEN THROUGH OLLAMA
# --------------------------------

chat_url = "http://localhost:11434/api/chat"

chat_payload = {
    "model": "gemma:2b",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False
}

chat_response = requests.post(
    chat_url,
    json=chat_payload
)

chat_data = chat_response.json()


# --------------------------------
# 8. GET FINAL ANSWER
# --------------------------------

answer = chat_data["message"]["content"]


print("\nFinal Answer:")
print("==============================")
print(answer)