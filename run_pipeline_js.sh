#!/bin/bash
# run_pipeline_js.sh
# Complete long-form pipeline for generating YouTube videos (JavaScript version)

echo "🎬 YouTube Automation Pipeline (JS)"
echo "===================================="
echo ""

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Step 1: Generate Script
echo "📝 Step 1/5: Generating script..."
node pipeline_js/script_generator.js
if [ $? -ne 0 ]; then
    echo "❌ Script generation failed!"
    exit 1
fi
echo ""

# Step 2: Fetch Images
echo "🖼️  Step 2/5: Fetching images..."
node pipeline_js/image_fetcher.js
if [ $? -ne 0 ]; then
    echo "❌ Image fetching failed!"
    exit 1
fi
echo ""

# Step 3: Generate Voice
# (Note: Using the existing shorts voice generator logic or adapting it for long-form if needed)
echo "🎙️  Step 3/5: Generating voice narration..."
node pipeline_js/shorts_voice_generator.js output/script.txt output/audio.wav
if [ $? -ne 0 ]; then
    echo "❌ Voice generation failed!"
    exit 1
fi
echo ""

# Step 4: Create Video
echo "🎥 Step 4/5: Assembling video..."
node pipeline_js/video_assembler.js
if [ $? -ne 0 ]; then
    echo "❌ Video assembly failed!"
    exit 1
fi
echo ""

# Step 5: Generate SEO Metadata
echo "🏷️  Step 5/5: Generating SEO metadata..."
node pipeline_js/seo.js
if [ $? -ne 0 ]; then
    echo "❌ SEO generation failed!"
    exit 1
fi
echo ""

echo "✅ Full YouTube video (JS) complete!"
echo "📁 Output files in output/ directory."
