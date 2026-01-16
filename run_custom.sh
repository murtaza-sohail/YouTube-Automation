#!/bin/bash
set -e

# Activate virtual environment
source .venv/bin/activate

# Load API keys
if [ -f .env ]; then
    set -a
    source .env
    set +a
    export PYTHONPATH=$PYTHONPATH:.
fi

echo "=========================================="
echo "Starting Custom YouTube Video Pipeline"
echo "=========================================="

echo "[1/3] Fetching Images..."
python3 -m pipeline.image_fetcher

echo "[2/3] Generating Voiceover (Rachel - Female)..."
python3 -m pipeline.voice_generator

echo "[3/3] Assembling Video (Fast, No Subtitles)..."
python3 -m pipeline.video_assembler_fast

echo "=========================================="
echo "Done! check output/final_video.mp4"
echo "=========================================="
