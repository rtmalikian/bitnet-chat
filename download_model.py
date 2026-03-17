from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="microsoft/BitNet-b1.58-2B-4T-gguf",
    local_dir="models/BitNet-b1.58-2B-4T"
)
print("Model downloaded successfully!")
