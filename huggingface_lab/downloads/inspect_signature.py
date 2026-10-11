import inspect
from huggingface_hub import snapshot_download

print(inspect.signature(snapshot_download))