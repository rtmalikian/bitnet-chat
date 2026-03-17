from huggingface_hub import snapshot_download

# Download TL1 quantized model for ARM/M1
snapshot_download(
    repo_id="microsoft/BitNet-b1.58-2B-4T-gguf",
    local_dir="models/BitNet-b1.58-2B-4T-tl1",
    allow_patterns="*tl1*"
)
print("TL1 model downloaded successfully!")
