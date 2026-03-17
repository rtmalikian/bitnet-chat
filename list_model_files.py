from huggingface_hub import list_repo_files

files = list_repo_files(repo_id="microsoft/BitNet-b1.58-2B-4T-gguf")
print("Available files in microsoft/BitNet-b1.58-2B-4T-gguf:")
for f in files:
    print(f"  - {f}")
