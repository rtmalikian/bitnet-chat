#!/bin/bash
# Quick start script for BitNet Web Server
# This script helps you set up and run the BitNet web interface

set -e

echo "🤖 BitNet Web Server - Quick Start"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker and Docker Compose found"
    USE_DOCKER=true
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker with built-in Compose found"
    USE_DOCKER=true
    COMPOSE_CMD="docker compose"
else
    echo -e "${YELLOW}!${NC} Docker not found, will use Python directly"
    USE_DOCKER=false
fi

# Check if model exists
MODEL_DIR="models/BitNet-b1.58-2B-4T"
MODEL_FILE="$MODEL_DIR/ggml-model-i2_s.gguf"

if [ ! -f "$MODEL_FILE" ]; then
    echo ""
    echo -e "${YELLOW}!${NC} Model not found at $MODEL_FILE"
    echo ""
    echo "Downloading model from Hugging Face..."
    
    mkdir -p "$MODEL_DIR"
    
    if command -v python3 &> /dev/null; then
        python3 -c "
from huggingface_hub import snapshot_download
print('Downloading model (this may take a few minutes)...')
snapshot_download(
    repo_id='microsoft/BitNet-b1.58-2B-4T-gguf',
    local_dir='$MODEL_DIR'
)
print('Model downloaded successfully!')
"
    else
        echo -e "${RED}✗${NC} Python3 is required to download the model"
        echo "Please install Python 3.9+ and try again"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Model found"
fi

echo ""

if [ "$USE_DOCKER" = true ]; then
    echo "🐳 Starting BitNet with Docker..."
    echo ""
    echo "Building Docker image (first time may take 10-20 minutes)..."
    echo ""
    
    if [ -z "$COMPOSE_CMD" ]; then
        docker-compose up --build
    else
        $COMPOSE_CMD up --build
    fi
else
    echo "🐍 Starting BitNet with Python..."
    echo ""
    
    # Check if virtual environment exists
    if [ -d "bitnet_venv" ]; then
        echo "Activating virtual environment..."
        source bitnet_venv/bin/activate
    fi
    
    # Install web server dependencies
    echo "Installing web server dependencies..."
    pip install -q fastapi uvicorn pydantic
    
    echo ""
    echo "Starting server..."
    echo ""
    echo -e "${GREEN}✓${NC} Web server starting at http://localhost:8080"
    echo ""
    
    python web_server/app.py
fi
