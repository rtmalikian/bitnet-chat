# BitNet Web Server Docker Image
# A ChatGPT-like interface for BitNet model running locally

FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    clang \
    pkg-config \
    libssl-dev \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as default
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3
RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy only the files needed for building llama.cpp first (to leverage cache)
COPY CMakeLists.txt .
COPY 3rdparty ./3rdparty
COPY include ./include
COPY src ./src
COPY preset_kernels ./preset_kernels

# Initialize and update git submodules
RUN cd 3rdparty/llama.cpp && git submodule update --init --recursive

# Build llama.cpp from source
RUN mkdir -p build && \
    cd build && \
    cmake .. \
        -DCMAKE_C_COMPILER=clang \
        -DCMAKE_CXX_COMPILER=clang++ \
        -DBITNET_ARM_TL1=ON \
        -DCMAKE_BUILD_TYPE=Release && \
    cmake --build . --config Release -j$(nproc)

# Copy the rest of the application
COPY web_server ./web_server
COPY utils ./utils
COPY models ./models

# Install Python dependencies for the web server
RUN pip3 install --no-cache-dir -r web_server/requirements.txt

# Install gguf package (needed for model handling)
RUN pip3 install --no-cache-dir gguf

# Expose the web server port
EXPOSE 8080

# Set environment variables
ENV MODEL_PATH=/app/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf
ENV CTX_SIZE=2048
ENV N_PREDICT=512
ENV TEMPERATURE=0.8
ENV THREADS=4

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the web server
CMD ["python3", "web_server/app.py"]
