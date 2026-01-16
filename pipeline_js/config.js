// pipeline_js/config.js
require('dotenv').config();

module.exports = {
    CHATGPT_API_KEY: process.env.CHATGPT_API_KEY,
    PEXELS_API_KEY: process.env.PEXELS_API_KEY,
    ELEVENLABS_API_KEY: process.env.ELEVENLABS_API_KEY,

    // Pipeline parameters
    IMAGE_DURATION_SECONDS: 3,
    VIDEO_RESOLUTION: "1080x1920", // Vertical for Shorts
    BACKGROUND_MUSIC_PATH: "assets/background.mp3",
    BEAT_DROP_TIMESTAMP: 120,

    // Output paths
    OUTPUT_DIR: "output",
    SHORTS_IMAGES_DIR: "output/shorts_images",
    SHORTS_SCRIPT_PATH: "output/shorts_script.txt",
    SHORTS_AUDIO_PATH: "output/shorts_audio.wav",
    SHORTS_FINAL_VIDEO: "output/shorts_final_js.mp4",
    SHORTS_METADATA_PATH: "output/shorts_metadata_js.txt"
};
