# BitNet Chat

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

### 📊 What's Microsoft's vs. What's Mine

| Component | Created By |
|-----------|------------|
| BitNet Model Architecture | **Microsoft Research** |
| Quantization Kernels (i2_s, TL1, TL2) | **Microsoft Research** |
| llama.cpp Integration | **Microsoft + llama.cpp team** |
| Command-line Inference | **Microsoft** |
| **Web Chat Interface** | **Raphael Tomas Malikian** ✋ |
| **FastAPI Web Server** | **Raphael Tomas Malikian** ✋ |
| **OpenAI-Compatible API Layer** | **Raphael Tomas Malikian** ✋ |
| **Docker Configuration** | **Raphael Tomas Malikian** ✋ |

---

## 📸 Screenshots

### Welcome Screen

![Welcome Screen](web_server/assets/screenshot1.png)

*The BitNet Chat welcome screen with suggestion cards for quick start.*

### Example: Explaining Quantum Computing

![Quantum Computing Explanation](web_server/assets/screenshot2.png)

*BitNet explaining quantum computing in simple terms - all processed locally on your machine.*

### Example: Python Code Generation

![Python Code Generation](web_server/assets/screenshot3.png)

*BitNet generating a Python script to sort numbers - with clear code examples.*

---

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/rtmalikian/bitnet-chat.git
cd bitnet-chat

# Install Python dependencies for web server
pip install fastapi uvicorn pydantic

# Start the web server
python web_server/app.py

# Open your browser to http://localhost:8080
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

---

## 💻 Usage

### Web Interface

1. Open http://localhost:8080 in your browser
2. Type a message or click a suggestion card
3. Chat with BitNet locally!

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

---

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

response = llm.invoke("Explain quantum computing in simple terms")
print(response.content)
```

### LlamaIndex

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    api_key="not-needed",
    api_base="http://localhost:8080/v1",
    model="bitnet",
    temperature=0.7
)

response = llm.complete("What is the capital of France?")
print(response.text)
```

---

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

---

## 📊 Performance

### Benchmarks on Apple M1 (2021 iMac)

| Metric | Value |
|--------|-------|
| Model | BitNet-b1.58-2B-4T (Microsoft) |
| Quantization | i2_s (2-bit) |
| Prompt Processing | ~25 tokens/sec |
| Text Generation | ~13-15 tokens/sec |
| Memory Usage | ~1.2 GB RAM |
| Model Size | 1.19 GB |

---

## 📁 Project Structure

```
bitnet-chat/
├── web_server/
│   ├── app.py              # FastAPI web server (My contribution)
│   ├── static/
│   │   └── index.html      # Web UI - ChatGPT-like interface (My contribution)
│   ├── assets/
│   │   └── screenshots*.png # Demo screenshots
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Detailed documentation
├── Dockerfile              # Docker image definition (My contribution)
├── docker-compose.yml      # Docker Compose configuration (My contribution)
├── start_web_server.sh     # Quick start script (My contribution)
├── models/                 # BitNet model files (Microsoft)
└── build/                  # Compiled llama.cpp binaries (Microsoft/llama.cpp)
```

---

## 🔒 Privacy & Security

**All inference happens locally on your machine.** No data is sent to external servers, cloud services, or third parties.

- ✅ No API keys required
- ✅ No internet connection needed (after initial setup)
- ✅ All conversation history stored locally in browser
- ✅ Model runs entirely on your hardware
- ✅ No telemetry or analytics

---

## 🛠️ Troubleshooting

### Common Issues

#### "Address already in use" error

```bash
# Kill the process using port 8080
lsof -ti:8080 | xargs kill -9

# Restart the server
python web_server/app.py
```

#### "Model file not found" error

```bash
# Verify model exists
ls -la models/BitNet-b1.58-2B-4T/

# Re-download if necessary
python -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/BitNet-b1.58-2B-4T-gguf', local_dir='models/BitNet-b1.58-2B-4T')"
```

#### Browser shows old version

- Hard refresh: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- Clear browser cache
- Try incognito/private mode

---

## 🙏 Acknowledgments

This project builds upon excellent work by others:

- **[Microsoft Research](https://github.com/microsoft/BitNet)** - For the amazing BitNet model and inference engine
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - For the efficient C++ inference framework
- **[OpenAI](https://openai.com)** - For the API design inspiration
- **[FastAPI](https://fastapi.tiangolo.com)** - For the excellent web framework

---

## 👨‍💻 Author

**Raphael Tomas Malikian**  
📍 Palmdale, California, USA  
📧 [rtmalikian@gmail.com](mailto:rtmalikian@gmail.com)  
🔗 [GitHub](https://github.com/rtmalikian)

**What I Built:**
- Web-based ChatGPT-like interface
- FastAPI server with OpenAI-compatible endpoints
- Docker configuration for easy deployment
- Responsive UI with conversation history

**What Microsoft Built:**
- BitNet model architecture
- Quantization kernels
- Command-line inference tools
- llama.cpp integration

---

## 📄 License

This web interface project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The underlying BitNet model and inference engine are subject to Microsoft's licensing terms.

---

## 📚 Resources

- **[Original BitNet Repository](https://github.com/microsoft/BitNet)** - Microsoft's official project
- **[BitNet Paper](https://arxiv.org/abs/2410.16144)** - Technical details on 1-bit LLMs
- **[Hugging Face Model](https://huggingface.co/microsoft/BitNet-b1.58-2B-4T-gguf)** - Download models
- **[llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)** - Inference engine docs

---

**Made with ❤️ by Raphael Tomas Malikian**

*Run AI locally, keep your data private.*
