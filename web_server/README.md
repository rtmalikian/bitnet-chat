# BitNet Chat - Web Interface

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker)](https://www.docker.com/)

**🤖 A ChatGPT-like web interface for Microsoft BitNet. Run a local AI assistant on your machine with OpenAI-compatible API. 100% private, no cloud required.**

> **⚠️ Important:** This project provides a **web interface tool** for Microsoft's BitNet model. The BitNet model and inference engine are developed by Microsoft. This project adds a user-friendly web UI layer on top of the existing BitNet infrastructure.

## 🔗 Original Project

This web interface is built on top of the official **Microsoft BitNet** project:

- **Original Repository:** [microsoft/BitNet](https://github.com/microsoft/BitNet)
- **Research Paper:** [BitNet: Scaling 1-bit Transformers](https://arxiv.org/abs/2310.11453)
- **Model:** [BitNet-b1.58-2B-4T on Hugging Face](https://huggingface.co/microsoft/BitNet-b1.58-2B-4T-gguf)

## 🎯 What This Project Adds

I created this **web-based ChatGPT-like interface** to make BitNet more accessible and user-friendly:

### ✨ New Features (My Contribution)

- 🎨 **Modern Web UI** - ChatGPT-style chat interface with conversation history
- 🔌 **OpenAI-Compatible API** - REST endpoints that work with LangChain, LlamaIndex, etc.
- 💬 **Browser-Based Chat** - No command line needed, chat directly in your browser
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🐳 **Docker Support** - One-command deployment
- 🔒 **Privacy-Focused** - All inference stays on your local machine

![BitNet Chat Demo](https://img.shields.io/badge/BitNet-b1.58--2B--4T-green)
![Performance](https://img.shields.io/badge/performance-~15_tokens/sec-orange)
![Privacy](https://img.shields.io/badge/privacy-100%25_local-brightgreen)

## ✨ Features

- 🎨 **Modern ChatGPT-like UI** - Clean, intuitive interface with conversation history
- 🔒 **100% Local & Private** - All inference happens on your machine, no data leaves your device
- 🚀 **OpenAI-Compatible API** - Use with LangChain, LlamaIndex, or any OpenAI client library
- 💬 **Conversation History** - Automatically saved in your browser's local storage
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast Performance** - Optimized for ARM CPUs (Apple Silicon) with ~15 tokens/sec
- 🐳 **Docker Ready** - One-command deployment with Docker Compose
- 🔌 **Easy Integration** - REST API endpoints for custom applications

## 📸 Screenshots

### Welcome Screen

![Welcome Screen](assets/screenshot1.png)

*The BitNet Chat welcome screen with suggestion cards for quick start.*

### Example: Explaining Quantum Computing

![Quantum Computing Explanation](assets/screenshot2.png)

*BitNet explaining quantum computing in simple terms - all processed locally on your machine.*

### Example: Python Code Generation

![Python Code Generation](assets/screenshot3.png)

*BitNet generating a Python script to sort numbers - with clear code examples.*

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/microsoft/BitNet.git
cd BitNet

# Install Python dependencies
pip install fastapi uvicorn pydantic

# Start the web server
python web_server/app.py
```

### Option 2: Docker (Recommended for Production)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8080
```

### Option 3: Quick Start Script

```bash
# Automated setup and launch
./start_web_server.sh
```

**👉 Access the web interface:** http://localhost:8080

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- CMake 3.22+ (for building llama.cpp)
- Clang 18+ (recommended compiler)
- 4GB+ RAM (model requires ~1.2GB)

### Step-by-Step Setup

1. **Install system dependencies:**

```bash
# macOS (with Homebrew)
brew install cmake pkg-config

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y cmake clang pkg-config
```

2. **Install Python dependencies:**

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install fastapi uvicorn pydantic
```

3. **Download the model:**

```bash
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='microsoft/BitNet-b1.58-2B-4T-gguf',
    local_dir='models/BitNet-b1.58-2B-4T'
)
"
```

4. **Launch the server:**

```bash
python web_server/app.py
```

## 💻 Usage

### Web Interface

Open http://localhost:8080 in your browser and start chatting!

**Features:**
- Click "New chat" to start a fresh conversation
- Conversation history is automatically saved
- Click on any previous conversation to resume it
- Use the "Clear" button to reset the current chat

### API Endpoints

#### Chat Completions

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bitnet",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.8,
    "max_tokens": 512
  }'
```

#### List Models

```bash
curl http://localhost:8080/v1/models
```

#### Health Check

```bash
curl http://localhost:8080/health
```

## 🔌 Integration Examples

### Python with OpenAI Client

```python
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",
    base_url="http://localhost:8080/v1"
)

response = client.chat.completions.create(
    model="bitnet",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to reverse a string"}
    ],
    temperature=0.7,
    max_tokens=256
)

print(response.choices[0].message.content)
```

### LangChain

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key="not-needed",
    openai_api_base="http://localhost:8080/v1",
    model_name="bitnet",
    temperature=0.7
)

# Simple invocation
response = llm.invoke("Explain quantum computing in simple terms")
print(response.content)

# Or use in a chain
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm
result = chain.invoke({"input": "What is the capital of France?"})
print(result.content)
```

### LlamaIndex

```python
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

# Configure BitNet as the LLM
llm = OpenAI(
    api_key="not-needed",
    api_base="http://localhost:8080/v1",
    model="bitnet",
    temperature=0.7
)

Settings.llm = llm

# Use with LlamaIndex
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Query
response = query_engine.query("What is this document about?")
print(response)
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8080/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'bitnet',
    messages: [
      { role: 'user', content: 'Hello!' }
    ]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to the GGUF model file | `models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| `CTX_SIZE` | Context window size (tokens) | `2048` |
| `N_PREDICT` | Max tokens to generate | `512` |
| `TEMPERATURE` | Sampling temperature (0.0-2.0) | `0.8` |
| `THREADS` | Number of CPU threads | `4` |

### Example with Custom Settings

```bash
# Run with custom configuration
export MODEL_PATH="./models/custom-model.gguf"
export THREADS=8
export CTX_SIZE=4096
export TEMPERATURE=0.5

python web_server/app.py
```

### Docker Compose Configuration

```yaml
services:
  bitnet-chat:
    image: bitnet-chat:latest
    ports:
      - "8080:8080"
    volumes:
      - ./models:/app/models
      - ./build:/app/build
    environment:
      - MODEL_PATH=/app/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf
      - THREADS=8
      - CTX_SIZE=2048
      - TEMPERATURE=0.7
    restart: unless-stopped
```

## 📊 Performance

### Benchmarks on Apple M1 (2021 iMac)

| Metric | Value |
|--------|-------|
| Model | BitNet-b1.58-2B-4T |
| Quantization | i2_s (2-bit) |
| Prompt Processing | ~25 tokens/sec |
| Text Generation | ~13-15 tokens/sec |
| Memory Usage | ~1.2 GB RAM |
| Model Size | 1.19 GB |

### Performance Tips

1. **Increase threads** for faster inference:
   ```bash
   export THREADS=8  # Or number of CPU cores
   ```

2. **Reduce context size** for lower memory usage:
   ```bash
   export CTX_SIZE=1024
   ```

3. **Lower temperature** for more deterministic outputs:
   ```bash
   export TEMPERATURE=0.5
   ```

## 🛠️ Troubleshooting

### Common Issues

#### "Address already in use" error

```bash
# Kill the process using port 8080
lsof -ti:8080 | xargs kill -9

# Or use a different port
export PORT=8081
python web_server/app.py --port $PORT
```

#### "Model file not found" error

```bash
# Verify model exists
ls -la models/BitNet-b1.58-2B-4T/

# Re-download if necessary
python -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/BitNet-b1.58-2B-4T-gguf', local_dir='models/BitNet-b1.58-2B-4T')"
```

#### Slow performance

- Ensure you're using the quantized model (i2_s)
- Increase thread count: `export THREADS=8`
- Close other memory-intensive applications
- Consider reducing context size

#### Docker build fails

```bash
# Clear Docker cache
docker-compose down
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Browser shows garbage output

- Hard refresh: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- Clear browser cache
- Try incognito/private mode

## 📁 Project Structure

```
bitnet/
├── web_server/
│   ├── app.py              # FastAPI web server
│   ├── static/
│   │   └── index.html      # Web UI (ChatGPT-like interface)
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # This file
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── start_web_server.sh     # Quick start script
├── models/
│   └── BitNet-b1.58-2B-4T/
│       └── ggml-model-i2_s.gguf  # Model file
└── build/                  # Compiled llama.cpp binaries
```

## 🔒 Privacy & Security

**All inference happens locally on your machine.** No data is sent to external servers, cloud services, or third parties.

- ✅ No API keys required
- ✅ No internet connection needed (after initial setup)
- ✅ All conversation history stored locally in browser
- ✅ Model runs entirely on your hardware
- ✅ No telemetry or analytics

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Areas for Contribution

- [ ] Streaming response support
- [ ] Multi-model support
- [ ] Enhanced UI features
- [ ] Performance optimizations
- [ ] Additional language support
- [ ] Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Microsoft](https://github.com/microsoft/BitNet)** - For the amazing BitNet model and research
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - For the efficient C++ inference engine
- **[OpenAI](https://openai.com)** - For the API design inspiration
- **[FastAPI](https://fastapi.tiangolo.com)** - For the excellent web framework

## 📚 Resources

- [BitNet Paper](https://arxiv.org/abs/2410.16144) - Technical details on 1-bit LLMs
- [Hugging Face Model](https://huggingface.co/microsoft/BitNet-b1.58-2B-4T-gguf) - Download models
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp) - Inference engine docs
- [FastAPI Documentation](https://fastapi.tiangolo.com) - Web framework guide

## 👨‍💻 Author

**Raphael Tomas Malikian**  
📍 Palmdale, California, USA  
📧 [rtmalikian@gmail.com](mailto:rtmalikian@gmail.com)  
🔗 [GitHub](https://github.com/rtmalikian)

**What I Built:**
- ✅ Web-based ChatGPT-like interface
- ✅ FastAPI server with OpenAI-compatible endpoints
- ✅ Docker configuration for easy deployment
- ✅ Responsive UI with conversation history

**What Microsoft Built:**
- 🔹 BitNet model architecture
- 🔹 Quantization kernels (i2_s, TL1, TL2)
- 🔹 Command-line inference tools
- 🔹 llama.cpp integration

## 📬 Support

- **Issues:** Open an issue on [GitHub](https://github.com/rtmalikian/bitnet-chat/issues) (for this web interface)
- **BitNet Issues:** [microsoft/BitNet Issues](https://github.com/microsoft/BitNet/issues) (for the model/inference engine)

---

**Made with ❤️ by Raphael Tomas Malikian**

*This project provides a web interface for Microsoft BitNet. BitNet itself is developed by Microsoft Research.*

*Run AI locally, keep your data private.*
