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

# Step 1: Prepare chat messages
messages = [
    {
        "role": "system",
        "content": "You are an IntelliStay hotel assistant. Answer briefly."
    },
    {
        "role": "user",
        "content": "What is a hotel reservation?"
    }
]

# Step 2: Convert messages into model inputs
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True
)

# Step 3: Check input structure
print("Input Type:", type(inputs))
print("Input Shape:", inputs["input_ids"].shape)

# Step 4: Generate answer
generated_ids = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=False
)

# Step 5: Extract newly generated tokens
response_ids = generated_ids[0][
    inputs["input_ids"].shape[1]:
]

# Step 6: Decode the answer
answer = tokenizer.decode(
    response_ids,
    skip_special_tokens=True
)

print("Qwen Answer:", answer)