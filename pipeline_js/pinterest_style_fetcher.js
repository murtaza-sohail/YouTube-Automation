// pipeline_js/pinterest_style_fetcher.js
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const config = require('./config');

const API_URL = "https://api.pexels.com/v1/search";

const KEYWORDS = [
    "meditation peaceful",
    "gratitude journal",
    "mindfulness nature",
    "peaceful morning",
    "thankful sunset",
    "calm ocean",
    "serene forest",
    "peaceful garden",
    "grateful hands",
    "meditation sunrise",
    "peaceful lake",
    "thankful prayer",
    "calm mountains",
    "peaceful flowers",
    "gratitude heart",
    "mindful breathing",
    "peaceful sky",
    "thankful smile",
    "calm waterfall",
    "peaceful candle"
];

async function fetchShortsImages(outputDir = config.SHORTS_IMAGES_DIR, numImages = 20) {
    console.log(`🖼️ Fetching ${numImages} portrait images for YouTube Shorts...`);

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    let imgIndex = 1;
    const imagesPerKeyword = Math.max(1, Math.floor(numImages / KEYWORDS.length));
    const headers = { Authorization: config.PEXELS_API_KEY };

    for (const kw of KEYWORDS) {
        if (imgIndex > numImages) break;

        try {
            const resp = await axios.get(API_URL, {
                headers,
                params: {
                    query: kw,
                    orientation: "portrait",
                    size: "large",
                    per_page: imagesPerKeyword
                },
                timeout: 10000
            });

            const photos = resp.data.photos || [];
            for (const photo of photos) {
                if (imgIndex > numImages) break;

                const imgUrl = photo.src.portrait;
                const imageResp = await axios.get(imgUrl, { responseType: 'arraybuffer', timeout: 10000 });

                const fileName = `img_${String(imgIndex).padStart(4, '0')}.jpg`;
                const filePath = path.join(outputDir, fileName);

                fs.writeFileSync(filePath, Buffer.from(imageResp.data));
                console.log(`  ✓ Saved ${fileName} (${kw})`);
                imgIndex++;
            }
        } catch (error) {
            console.warn(`  ⚠ Warning: Failed to fetch '${kw}': ${error.message}`);
            continue;
        }
    }

    const totalDownloaded = imgIndex - 1;
    console.log(`\n✓ Downloaded ${totalDownloaded} images to ${outputDir}`);
    return outputDir;
}

if (require.main === module) {
    fetchShortsImages().catch(err => process.exit(1));
}

module.exports = { fetchShortsImages };
