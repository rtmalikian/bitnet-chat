"""
BitNet Web Server - A ChatGPT-like interface for BitNet model
"""
import os
import sys
import json
import signal
import asyncio
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import time

app = FastAPI(title="BitNet API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = os.environ.get("MODEL_PATH", "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf")
CTX_SIZE = int(os.environ.get("CTX_SIZE", "2048"))
N_PREDICT = int(os.environ.get("N_PREDICT", "512"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.8"))
THREADS = int(os.environ.get("THREADS", "4"))

# Conversation history storage
conversations: Dict[str, List[Dict[str, str]]] = {}


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "bitnet"
    messages: List[Message]
    temperature: float = TEMPERATURE
    top_p: float = 0.95
    n: int = 1
    stream: bool = False
    stop: Optional[List[str]] = None
    max_tokens: Optional[int] = N_PREDICT
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0


class ChatMessage(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Usage] = None


class ChatChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[Dict[str, Any]]


def build_prompt(messages: List[Message]) -> str:
    """Convert OpenAI-style messages to a prompt string."""
    prompt_parts = []
    for msg in messages:
        if msg.role == "system":
            prompt_parts.append(f"System: {msg.content}")
        elif msg.role == "user":
            prompt_parts.append(f"User: {msg.content}")
        elif msg.role == "assistant":
            prompt_parts.append(f"Assistant: {msg.content}")
    
    prompt_parts.append("Assistant:")
    return "\n".join(prompt_parts)


def run_llama_cli(prompt: str, n_predict: int = N_PREDICT, temp: float = TEMPERATURE):
    """Run the llama-cli command and return the generated text."""
    build_dir = "build"
    cli_path = os.path.join(build_dir, "bin", "llama-cli")
    
    if not os.path.exists(cli_path):
        cli_path = os.path.join(build_dir, "bin", "Release", "llama-cli")
    
    if not os.path.exists(cli_path):
        raise FileNotFoundError(f"llama-cli not found at {cli_path}")
    
    cmd = [
        cli_path,
        "-m", MODEL_PATH,
        "-c", str(CTX_SIZE),
        "-t", str(THREADS),
        "-n", str(n_predict),
        "--temp", str(temp),
        "-p", prompt,
        "-b", "1",
        "--no-display-prompt",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise TimeoutError("Model generation timed out")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the web interface."""
    static_path = Path("web_server/static")
    html_path = static_path / "index.html"

    if html_path.exists():
        response = HTMLResponse(content=html_path.read_text())
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    # Fallback inline HTML
    return HTMLResponse(content=get_fallback_html())


def get_fallback_html():
    """Fallback HTML if static files are not found."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitNet Chat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #343541;
            color: #ececf1;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        .sidebar {
            width: 260px;
            background: #202123;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }
        .new-chat-btn {
            background: transparent;
            border: 1px solid #565869;
            color: #ececf1;
            padding: 12px;
            border-radius: 5px;
            cursor: pointer;
            text-align: left;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .new-chat-btn:hover { background: #2a2b32; }
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding-bottom: 150px;
        }
        .message {
            padding: 24px;
            display: flex;
            gap: 20px;
            border-bottom: 1px solid #2a2b32;
        }
        .message.user { background: #343541; }
        .message.assistant { background: #444654; }
        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        .user .avatar { background: #5436DA; }
        .assistant .avatar { background: #19C37D; }
        .content {
            flex: 1;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        .input-container {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, #343541 20%);
            padding: 24px;
        }
        .input-box {
            max-width: 768px;
            margin: 0 auto;
            position: relative;
        }
        textarea {
            width: 100%;
            background: #40414f;
            border: 1px solid #565869;
            color: #ececf1;
            padding: 14px 45px 14px 16px;
            border-radius: 12px;
            resize: none;
            font-family: inherit;
            font-size: 16px;
            line-height: 1.5;
            outline: none;
            max-height: 200px;
            min-height: 52px;
        }
        textarea:focus { border-color: #8e8ea0; }
        .send-btn {
            position: absolute;
            right: 12px;
            bottom: 12px;
            background: transparent;
            border: none;
            color: #8e8ea0;
            cursor: pointer;
            padding: 5px;
        }
        .send-btn:hover { color: #ececf1; }
        .send-btn:disabled { opacity: 0.3; cursor: not-allowed; }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #ececf1;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .model-info {
            padding: 10px;
            text-align: center;
            font-size: 12px;
            color: #8e8ea0;
            border-bottom: 1px solid #2a2b32;
        }
        h1 { font-size: 20px; margin-bottom: 5px; }
        p { font-size: 14px; }
    </style>
</head>
<body>
    <div class="model-info">
        <h1>🤖 BitNet Chat</h1>
        <p>Running BitNet-b1.58-2B-4T on your local machine</p>
    </div>
    <div class="container">
        <div class="sidebar">
            <button class="new-chat-btn" onclick="newChat()">
                <span>+</span> New chat
            </button>
        </div>
        <div class="main">
            <div class="chat-container" id="chatContainer"></div>
            <div class="input-container">
                <div class="input-box">
                    <textarea 
                        id="userInput" 
                        placeholder="Send a message..." 
                        rows="1"
                        onkeydown="handleKeyDown(event)"
                        oninput="autoResize(this)"
                    ></textarea>
                    <button class="send-btn" id="sendBtn" onclick="sendMessage()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
    <script>
        let conversationId = null;
        let messages = [];
        let isLoading = false;

        function autoResize(textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
        }

        function handleKeyDown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function newChat() {
            conversationId = null;
            messages = [];
            document.getElementById('chatContainer').innerHTML = '';
            document.getElementById('userInput').value = '';
        }

        function addMessage(role, content) {
            const container = document.getElementById('chatContainer');
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.innerHTML = `
                <div class="avatar">${role === 'user' ? 'U' : 'AI'}</div>
                <div class="content">${escapeHtml(content)}</div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const sendBtn = document.getElementById('sendBtn');
            const content = input.value.trim();
            
            if (!content || isLoading) return;
            
            isLoading = true;
            input.value = '';
            input.style.height = 'auto';
            sendBtn.disabled = true;
            
            addMessage('user', content);
            messages.push({ role: 'user', content });
            
            // Add loading message
            const container = document.getElementById('chatContainer');
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant';
            loadingDiv.id = 'loadingMessage';
            loadingDiv.innerHTML = `
                <div class="avatar">AI</div>
                <div class="content"><span class="loading"></span></div>
            `;
            container.appendChild(loadingDiv);
            container.scrollTop = container.scrollHeight;
            
            try {
                const response = await fetch('/v1/chat/completions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: 'bitnet',
                        messages: messages,
                        temperature: 0.8,
                        max_tokens: 512,
                        stream: false
                    })
                });
                
                const data = await response.json();
                
                // Remove loading message
                loadingDiv.remove();
                
                if (data.choices && data.choices.length > 0) {
                    const assistantMessage = data.choices[0].message.content;
                    addMessage('assistant', assistantMessage);
                    messages.push({ role: 'assistant', content: assistantMessage });
                } else {
                    addMessage('assistant', 'Error: No response from model');
                }
            } catch (error) {
                loadingDiv.remove();
                addMessage('assistant', `Error: ${error.message}`);
            }
            
            isLoading = false;
            sendBtn.disabled = false;
            input.focus();
        }

        // Auto-focus input on load
        window.onload = () => document.getElementById('userInput').focus();
    </script>
</body>
</html>"""


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint."""
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages array is required")

    prompt = build_prompt(request.messages)
    n_predict = request.max_tokens or N_PREDICT
    temp = request.temperature or TEMPERATURE

    conversation_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    if request.stream:
        # Streaming not yet supported - return non-streaming response
        pass

    # Non-streaming response
    try:
        # Run the model in a thread pool to avoid blocking
        import asyncio
        loop = asyncio.get_event_loop()
        generated_text = await loop.run_in_executor(
            None, run_llama_cli, prompt, n_predict, temp
        )

        response = ChatCompletionResponse(
            id=conversation_id,
            created=created,
            model=request.model or "bitnet",
            choices=[
                Choice(
                    index=0,
                    message=ChatMessage(role="assistant", content=generated_text),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=len(prompt.split()),
                completion_tokens=len(generated_text.split()),
                total_tokens=len(prompt.split()) + len(generated_text.split())
            )
        )
        return response

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Model generation timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_stream(prompt: str, conversation_id: str, created: int, model: str):
    """Generate streaming response."""
    try:
        process = run_llama_cli(prompt, N_PREDICT, TEMPERATURE)
        
        # Send initial chunk
        initial_chunk = {
            "id": conversation_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"role": "assistant"},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(initial_chunk)}\n\n"
        
        # Stream tokens
        output = ""
        for line in iter(process.stdout.readline, ''):
            if line:
                output += line
                chunk = {
                    "id": conversation_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": line},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
        
        # Final chunk
        final_chunk = {
            "id": conversation_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_chunk = {
            "error": {
                "message": str(e),
                "type": "server_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"


@app.get("/v1/models")
async def list_models():
    """OpenAI-compatible models endpoint."""
    return {
        "object": "list",
        "data": [
            {
                "id": "bitnet",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "microsoft",
                "permission": [],
                "root": "bitnet",
                "parent": None
            }
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_exists = os.path.exists(MODEL_PATH)
    return {
        "status": "healthy" if model_exists else "degraded",
        "model_loaded": model_exists,
        "model_path": MODEL_PATH
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
