import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

# Step 1: Load our downloaded Qwen model
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

# Step 2: Enter a sentence
text = "The guest booked a"

# Step 3: Convert sentence into token IDs
inputs = tokenizer(text, return_tensors="pt")

# Step 4: Execute the model
with torch.no_grad():
    outputs = model(**inputs)

# Step 5: Retrieve next-token logits
logits = outputs.logits[0, -1, :]

# Step 6: Convert logits into probabilities
probabilities = torch.softmax(logits.float(), dim=-1)

# Step 7: Find the top 5 predicted tokens
top_probs, top_ids = torch.topk(probabilities, 5)

print("Input Sentence:", text)
print("Logits Shape:", logits.shape)

print("\nTop 5 Next Token Predictions:")

print("Tokens:", tokenizer.tokenize(text))
print("Total Tokens:", inputs["input_ids"].shape[1])

for token_id, probability in zip(top_ids, top_probs):
    token = tokenizer.decode([token_id.item()])

    print(
        repr(token),
        round(probability.item() * 100, 2),
        "%"
    )

   


generated_ids = model.generate(
    **inputs,
    max_new_tokens=20,
    do_sample=False
)

generated_text = tokenizer.decode(
    generated_ids[0],
    skip_special_tokens=True
)

print("Generated Text:", generated_text)

input_tokens = inputs["input_ids"].shape[1]

total_tokens = generated_ids.shape[1]

new_tokens = total_tokens - input_tokens

print("Input Tokens:", input_tokens)
print("Total Tokens:", total_tokens)
print("Generated Tokens:", new_tokens)