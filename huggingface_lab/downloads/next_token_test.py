import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = Path(__file__).resolve().parent / "model" / "qwen-mini"

tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    local_files_only=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    local_files_only=True
)

model.eval()

text = "The guest booked a"

inputs = tokenizer(
    text,
    return_tensors="pt"
)

with torch.no_grad():
    outputs = model(**inputs)

# Get scores for the next token
logits = outputs.logits[0, -1, :]

# Convert scores to probabilities
probabilities = torch.softmax(logits.float(), dim=-1)

# Find the 5 most probable tokens
top_probs, top_ids = torch.topk(probabilities, 5)

print("Input:", text)
print("\nTop 5 Next Token Predictions:")

for token_id, probability in zip(top_ids, top_probs):

    token = tokenizer.decode([token_id.item()])

    print(
        repr(token),
        ":",
        round(probability.item() * 100, 2),
        "%"
    )