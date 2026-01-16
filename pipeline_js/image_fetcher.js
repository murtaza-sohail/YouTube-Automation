// pipeline_js/image_fetcher.js
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const config = require('./config');

const API_URL = "https://api.pexels.com/v1/search";

const KEYWORDS = [
    "discipline gym", "dark room", "lonely man", "rain night city", "focus hard work",
    "clock ticking", "mountain peak", "running rain", "boxing training", "shadow boxing",
    "cold morning", "empty street night", "man in suit silhouette", "library studying", "chess player",
    "wolf howling", "eagle soaring", "lion roar", "stormy ocean", "burning fire",
    "ancient ruins", "modern office night", "sweat workout", "heavy weights", "tired face",
    "sunrise mountain", "stargazing", "bridge in fog", "forest mist", "desert road",
    "climbing rock", "lifting heavy", "underwater swimming", "fast car driving night", "city lights blur",
    "meditation", "praying", "writing journal", "drawing plans", "building structure",
    "gears turning", "compass", "map adventure", "climbing stairs", "tunnel light",
    "rain on window", "puddle reflection", "lightning storm", "snow mountain", "volcano lava",
    "old tree", "new sprout", "breaking chains", "wall breaking", "door opening",
    "clenched fist", "intense eyes", "staring mirror", "walking alone", "standing tall",
    "black and white portrait", "cinematic lighting", "gritty texture", "industrial site", "construction",
    "space nebula", "planet earth", "sunrise from space", "satellite", "rocket launch",
    "running track", "olympic stadium", "crowd cheering blur", "trophy", "medal",
    "sweeping floor", "washing dishes", "simple lifestyle", "asceticism", "stoicism",
    "fighting", "defense", "guards", "armor", "sword", "shield", "throne", "crown"
];

async function fetchImages(outputDir = path.join(config.OUTPUT_DIR, "images"), numImagesPerKeyword = 5) {
    console.log(`🖼️ Fetching landscape images for long-form video...`);

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    let imgIndex = 1;
    const headers = { Authorization: config.PEXELS_API_KEY };

    for (const kw of KEYWORDS) {
        try {
            const resp = await axios.get(API_URL, {
                headers,
                params: {
                    query: kw,
                    orientation: "landscape",
                    size: "large",
                    per_page: numImagesPerKeyword
                },
                timeout: 15000
            });

            const photos = resp.data.photos || [];
            for (const photo of photos) {
                const imgUrl = photo.src.large2x;
                const imageResp = await axios.get(imgUrl, { responseType: 'arraybuffer', timeout: 15000 });

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

    console.log(`\n✓ Downloaded ${imgIndex - 1} images to ${outputDir}`);
}

if (require.main === module) {
    fetchImages().catch(err => process.exit(1));
}

module.exports = { fetchImages };
