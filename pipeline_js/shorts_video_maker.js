// pipeline_js/shorts_video_maker.js
const path = require('path');
const fs = require('fs');
const ffmpeg = require('fluent-ffmpeg');
const config = require('./config');
const { execSync } = require('child_process');

async function makeShortsVideo(
    imageDir = config.SHORTS_IMAGES_DIR,
    audioPath = config.SHORTS_AUDIO_PATH,
    outputPath = config.SHORTS_FINAL_VIDEO
) {
    const images = fs.readdirSync(imageDir)
        .filter(f => f.endsWith('.jpg'))
        .sort()
        .map(f => path.join(imageDir, f));

    if (images.length === 0) {
        console.error("❌ No images found!");
        return null;
    }

    if (!fs.existsSync(audioPath)) {
        console.error("❌ Audio file not found!");
        return null;
    }

    console.log("Creating YouTube Shorts video (JS)...");

    // Get audio duration using ffprobe CLI (fastest way for sync)
    const durationOutput = execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${audioPath}`).toString();
    const audioDuration = parseFloat(durationOutput.trim());
    const durationPerImage = audioDuration / images.length;

    console.log(`  Images: ${images.length}`);
    console.log(`  Audio: ${audioPath}`);
    console.log(`  Audio duration: ${audioDuration.toFixed(1)} seconds`);
    console.log(`  Duration per image: ${durationPerImage.toFixed(2)} seconds`);

    // Create concat file for ffmpeg
    const concatPath = path.join(path.dirname(outputPath), "shorts_concat_js.txt");
    let concatContent = "";
    images.forEach(img => {
        concatContent += `file '${path.resolve(img)}'\nduration ${durationPerImage.toFixed(2)}\n`;
    });
    // Repeat last image to fix ffmpeg concat bug
    if (images.length > 0) {
        concatContent += `file '${path.resolve(images[images.length - 1])}'\n`;
    }
    fs.writeFileSync(concatPath, concatContent);

    console.log("\n🎬 Rendering vertical video (1080x1920) with fluent-ffmpeg...");

    return new Promise((resolve, reject) => {
        ffmpeg()
            .input(concatPath)
            .inputOptions(['-f concat', '-safe 0'])
            .input(audioPath)
            .videoFilters([
                'scale=1080:1920:force_original_aspect_ratio=decrease',
                'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black',
                'fps=30'
            ])
            .videoCodec('libx264')
            .outputOptions([
                '-preset medium',
                '-crf 23',
                '-pix_fmt yuv420p',
                '-shortest',
                '-movflags +faststart'
            ])
            .audioCodec('aac')
            .audioBitrate('128k')
            .save(outputPath)
            .on('end', () => {
                const sizeMb = fs.statSync(outputPath).size / (1024 * 1024);
                console.log(`\n✅ YouTube Shorts video ready!`);
                console.log(`   File: ${outputPath}`);
                console.log(`   Size: ${sizeMb.toFixed(1)} MB`);
                console.log(`   Format: 1080x1920 (9:16 vertical)`);
                fs.unlinkSync(concatPath);
                resolve(outputPath);
            })
            .on('error', (err) => {
                console.error(`\n❌ Video rendering failed: ${err.message}`);
                reject(err);
            });
    });
}

if (require.main === module) {
    makeShortsVideo().catch(err => process.exit(1));
}

module.exports = { makeShortsVideo };
