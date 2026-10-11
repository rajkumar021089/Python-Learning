import torch

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM


# STEP 1: Locate downloaded model

model_path = Path(__file__).resolve().parent / "model" / "qwen-mini"


# STEP 2: Load tokenizer

tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    local_files_only=True
)


# STEP 3: Load Qwen model

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    attn_implementation="eager",
    local_files_only=True
)

model.eval()


# STEP 4: Prepare sentences

sentences = [
    "I deposited money in the bank",
    "I sat beside the river bank"
]


# STEP 5: Process each sentence

for sentence in sentences:

    print("\n================================")
    print("SENTENCE:", sentence)
    print("================================")

    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        add_special_tokens=False
    )

    with torch.no_grad():

        output = model(
            **inputs,
            output_attentions=True,
            use_cache=False
        )

    attention = output.attentions

    tokens = tokenizer.convert_ids_to_tokens(
        inputs["input_ids"][0].tolist()
    )

    print("Total Layers:", len(attention))

    # STEP 6: Examine three layers

    for layer_number in [0, 12, 23]:

        print("\nLAYER:", layer_number + 1)

        weights = attention[layer_number][0, 0, -1, :]

        for token, weight in zip(tokens, weights):

            print(
                token,
                ":",
                round(weight.item(), 4)
            )