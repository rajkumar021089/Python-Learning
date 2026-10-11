from huggingface_hub import snapshot_download

model_name="Qwen/Qwen2.5-0.5B-Instruct"

print("Downloading model...")


model_path=snapshot_download(
    repo_id=model_name,
    local_dir="./model/qwen-mini"
)

print("Download completed!")
print("Model saved at:", model_path)


messages=[
    {
        "role": "system",
        "content": "You are a hotel reservation assistant."
    },
    {
        "role": "user",
        "content": "What is the difference between reservation and check-in?"
    }
]

