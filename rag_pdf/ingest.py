from pypdf import PdfReader
import requests

PDF_FILE = "IntelliStay_RAG_Sample.pdf"


# -------------------------
# 1. READ PDF
# -------------------------

reader = PdfReader(PDF_FILE)

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"


# -------------------------
# 2. CREATE CHUNKS
# -------------------------

def create_chunks(text, chunk_size=100, overlap=20):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start = end - overlap

    return chunks


chunks = create_chunks(full_text)

print("Total chunks:", len(chunks))


# -------------------------
# 3. CREATE EMBEDDINGS
# -------------------------

url = "http://localhost:11434/api/embed"

payload = {
    "model": "nomic-embed-text",
    "input": chunks
}

response = requests.post(url, json=payload)

data = response.json()

embeddings = data["embeddings"]


print("Total embeddings:", len(embeddings))

print("Vector size:", len(embeddings[0]))

print("\nFirst 10 numbers of Chunk 0 embedding:")

print(embeddings[0][:10])


import math


# -------------------------
# 4. EMBED A QUESTION
# -------------------------

question = "What happens to the room after checkout?"

question_payload = {
    "model": "nomic-embed-text",
    "input": question
}

question_response = requests.post(url, json=question_payload)

question_data = question_response.json()

question_embedding = question_data["embeddings"][0]


print("\nQuestion:")
print(question)

print("\nQuestion vector size:")
print(len(question_embedding))


# -------------------------
# 5. COSINE SIMILARITY
# -------------------------

def cosine_similarity(vector1, vector2):

    dot_product = sum(a * b for a, b in zip(vector1, vector2))

    magnitude1 = math.sqrt(sum(a * a for a in vector1))

    magnitude2 = math.sqrt(sum(b * b for b in vector2))

    return dot_product / (magnitude1 * magnitude2)


# -------------------------
# 6. COMPARE QUESTION
#    WITH EVERY CHUNK
# -------------------------

scores = []

for i, embedding in enumerate(embeddings):

    score = cosine_similarity(
        question_embedding,
        embedding
    )

    scores.append((i, score))

    print("Chunk", i, "Similarity:", score)


# -------------------------
# 7. SORT BEST MATCH FIRST
# -------------------------

scores.sort(
    key=lambda x: x[1],
    reverse=True
)


best_chunk_index = scores[0][0]

best_score = scores[0][1]


print("\nBEST MATCH")
print("====================")

print("Chunk:", best_chunk_index)

print("Score:", best_score)

print("\nRetrieved text:")

print(chunks[best_chunk_index])