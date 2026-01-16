#!/bin/bash
# run_shorts.sh
# Complete pipeline for generating YouTube Shorts video

echo "🎬 YouTube Shorts Generator - Patience & Gratitude"
echo "=================================================="
echo ""

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Step 1: Generate Script
echo "📝 Step 1/5: Generating script..."
python -m pipeline.shorts_script_generator
if [ $? -ne 0 ]; then
    echo "❌ Script generation failed!"
    exit 1
fi
echo ""

# Step 2: Fetch Images
echo "🖼️  Step 2/5: Fetching Pinterest-style images..."
python -m pipeline.pinterest_style_fetcher
if [ $? -ne 0 ]; then
    echo "❌ Image fetching failed!"
    exit 1
fi
echo ""

# Step 3: Generate Voice
echo "🎙️  Step 3/5: Generating male voice narration..."
python -m pipeline.shorts_voice_generator
if [ $? -ne 0 ]; then
    echo "❌ Voice generation failed!"
    exit 1
fi
echo ""

# Step 4: Create Video
echo "🎥 Step 4/5: Assembling vertical video..."
python -m pipeline.shorts_video_maker
if [ $? -ne 0 ]; then
    echo "❌ Video assembly failed!"
    exit 1
fi
echo ""

# Step 5: Generate SEO Metadata
echo "🏷️  Step 5/5: Generating SEO metadata..."
python -m pipeline.shorts_seo
if [ $? -ne 0 ]; then
    echo "❌ SEO generation failed!"
    exit 1
fi
echo ""

echo "✅ YouTube Shorts video complete!"
echo "📁 Output files:"
echo "   - Video: output/shorts_final.mp4"
echo "   - Script: output/shorts_script.txt"
echo "   - Audio: output/shorts_audio.wav"
echo "   - Metadata: output/shorts_metadata.txt"
echo ""
echo "🚀 Ready to upload to YouTube Shorts!"
