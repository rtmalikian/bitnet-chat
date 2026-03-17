# BitNet Docker Web Server - Quick Start Guide

## 🚀 What You Get

A fully containerized ChatGPT-like web interface for BitNet that runs 100% locally on your machine.

**Features:**
- Modern, responsive ChatGPT-like UI
- OpenAI-compatible REST API
- Conversation history (saved in browser)
- Docker containerization for easy deployment
- No data leaves your device

## 📦 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to the bitnet directory
cd /Users/raphael/Coding/bitnet

# Build and run
docker-compose up --build

# Access the web interface
open http://localhost:8080
```

### Option 2: Run Locally (Already Set Up)

```bash
# Activate your virtual environment
source bitnet_venv/bin/activate

# Start the web server
python web_server/app.py

# Or use the convenience script
./start_web_server.sh
```

## 🌐 Access Points

- **Web Interface:** http://localhost:8080
- **API Endpoint:** http://localhost:8080/v1/chat/completions
- **Health Check:** http://localhost:8080/health
- **Models API:** http://localhost:8080/v1/models

## 🔧 Configuration

Edit environment variables in `docker-compose.yml` or set them locally:

```bash
export MODEL_PATH="models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
export THREADS=4
export CTX_SIZE=2048
export TEMPERATURE=0.8
```

## 💻 API Usage Examples

### With curl

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bitnet",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### With Python OpenAI client

```python
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",
    base_url="http://localhost:8080/v1"
)

response = client.chat.completions.create(
    model="bitnet",
    messages=[
        {"role": "user", "content": "Write a Python hello world"}
    ]
)
print(response.choices[0].message.content)
```

### With LangChain

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key="not-needed",
    openai_api_base="http://localhost:8080/v1",
    model_name="bitnet"
)

response = llm.invoke("Explain quantum computing")
print(response.content)
```

## 🛑 Stop the Server

### Docker
```bash
docker-compose down
```

### Local
```bash
# Find and kill the process
lsof -ti:8080 | xargs kill -9
```

## 📁 File Structure

```
bitnet/
├── web_server/
│   ├── app.py              # FastAPI web server
│   ├── static/
│   │   └── index.html      # Web UI
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Detailed documentation
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── start_web_server.sh     # Quick start script
├── models/
│   └── BitNet-b1.58-2B-4T/
│       └── ggml-model-i2_s.gguf  # The model file
└── build/                  # Compiled llama.cpp binaries
```

## 🐛 Troubleshooting

### "Connection refused" on localhost:8080
- Make sure the server is running
- Check if another process is using port 8080: `lsof -i:8080`

### "Model not found"
- Ensure the model file exists at `models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf`
- Download it with: `python -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/BitNet-b1.58-2B-4T-gguf', local_dir='models/BitNet-b1.58-2B-4T')"`

### Docker build fails
- Make sure Docker Desktop is running
- Try: `docker-compose build --no-cache`

### Slow response times
- This is normal for a 2B parameter model on CPU
- Expected: 10-15 tokens/second on M1 Mac
- Increase threads: `export THREADS=8`

## 📊 Performance on Your M1 iMac

- **Model:** BitNet-b1.58-2B-4T (2.4B parameters)
- **Quantization:** i2_s (2-bit)
- **Expected Speed:** ~10-15 tokens/second
- **Memory Usage:** ~1.2 GB RAM

## 🔒 Privacy

All inference happens locally on your machine. No data is sent to external servers.

## 📚 Next Steps

1. **Explore the UI** - Open http://localhost:8080 and start chatting
2. **Try the API** - Use with your favorite AI tools
3. **Customize** - Modify temperature, context size, etc.
4. **Build something** - Create your own AI-powered applications

Enjoy your local AI assistant! 🎉
