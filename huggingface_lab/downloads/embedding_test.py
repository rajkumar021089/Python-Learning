from pathlib import Path
from transformers import AutoModelForCausalLM

model_path = Path(__file__).resolve().parent / "model" / "qwen-mini"

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    local_files_only=True
)

embedding_layer = model.get_input_embeddings()

token_id = 1072

vector = embedding_layer.weight[token_id]

print("Vector Shape:", vector.shape)
print("Total Values:", vector.numel())
print("First 5 Values:", vector[:5].tolist())