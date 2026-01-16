#!/bin/bash
set -e

# Activate virtual environment
source .venv/bin/activate

# Load API keys from .env file
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi 

# Ensure keys are present
if [ -z "$PEXELS_API_KEY" ] || [ -z "$CHATGPT_API_KEY" ] || [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "Error: API keys are missing. Please set them in a .env file or environment variables."
    exit 1
fi
export PATH="$PWD/bin:$PATH"

echo "=========================================="
echo "Starting YouTube Motivational Video Pipeline"
echo "=========================================="

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it to proceed."
    exit 1
fi

echo "[1/5] Generating Script..."
python3 -m pipeline.script_generator

echo "[2/5] Fetching Images..."
# The image_fetcher uses a default list if not provided, which matches the brief.
python3 -m pipeline.image_fetcher

echo "[3/5] Generating Voiceover..."
python3 -m pipeline.voice_generator

echo "[4/5] Assembling Video..."
python3 -m pipeline.video_assembler

echo "[5/5] Generating Metadata..."
python3 -m pipeline.seo

echo "[6/5] Uploading to YouTube..."
python3 -m pipeline.youtube_uploader

echo "=========================================="
echo "Pipeline Finished Successfully!"
echo "Output files are in the 'output' directory."
echo "=========================================="
