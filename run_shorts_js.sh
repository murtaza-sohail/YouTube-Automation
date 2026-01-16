#!/bin/bash
# run_shorts_js.sh
# Complete pipeline for generating YouTube Shorts video (JavaScript version)

echo "🎬 YouTube Shorts Generator (JS) - Patience & Gratitude"
echo "====================================================="
echo ""

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Step 1: Generate Script
echo "📝 Step 1/5: Generating script..."
node pipeline_js/shorts_script_generator.js
if [ $? -ne 0 ]; then
    echo "❌ Script generation failed!"
    exit 1
fi
echo ""

# Step 2: Fetch Images
echo "🖼️  Step 2/5: Fetching Pinterest-style images..."
node pipeline_js/pinterest_style_fetcher.js
if [ $? -ne 0 ]; then
    echo "❌ Image fetching failed!"
    exit 1
fi
echo ""

# Step 3: Generate Voice
echo "🎙️  Step 3/5: Generating male voice narration..."
node pipeline_js/shorts_voice_generator.js
if [ $? -ne 0 ]; then
    echo "❌ Voice generation failed!"
    exit 1
fi
echo ""

# Step 4: Create Video
echo "🎥 Step 4/5: Assembling vertical video..."
node pipeline_js/shorts_video_maker.js
if [ $? -ne 0 ]; then
    echo "❌ Video assembly failed!"
    exit 1
fi
echo ""

# Step 5: Generate SEO Metadata
echo "🏷️  Step 5/5: Generating SEO metadata..."
node pipeline_js/shorts_seo.js
if [ $? -ne 0 ]; then
    echo "❌ SEO generation failed!"
    exit 1
fi
echo ""

echo "✅ YouTube Shorts video (JS) complete!"
echo "📁 Output files:"
echo "   - Video: output/shorts_final_js.mp4"
echo "   - Script: output/shorts_script.txt"
echo "   - Audio: output/shorts_audio.wav"
echo "   - Metadata: output/shorts_metadata_js.txt"
echo ""
echo "🚀 Ready to upload to YouTube Shorts!"
