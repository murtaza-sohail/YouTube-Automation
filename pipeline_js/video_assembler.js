// pipeline_js/video_assembler.js
const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');
const config = require('./config');

async function assembleVideo(
    imageDir = path.join(config.OUTPUT_DIR, "images"),
    audioPath = path.join(config.OUTPUT_DIR, "audio.wav"),
    outputPath = path.join(config.OUTPUT_DIR, "final_video.mp4")
) {
    const images = fs.readdirSync(imageDir)
        .filter(f => f.endsWith('.jpg'))
        .sort()
        .map(f => path.join(imageDir, f));

    if (images.length === 0) {
        console.error("❌ No images found!");
        return null;
    }

    console.log("🎬 Assembling long-form video...");

    // Create a temporary concat file
    const concatPath = path.join(config.OUTPUT_DIR, "concat_long.txt");
    let concatContent = "";
    images.forEach(img => {
        concatContent += `file '${path.resolve(img)}'\nduration ${config.IMAGE_DURATION_SECONDS}\n`;
    });
    // Repeat last image
    concatContent += `file '${path.resolve(images[images.length - 1])}'\n`;
    fs.writeFileSync(concatPath, concatContent);

    return new Promise((resolve, reject) => {
        let command = ffmpeg()
            .input(concatPath)
            .inputOptions(['-f concat', '-safe 0'])
            .input(audioPath);

        // Add background music if it exists
        const bgmPath = config.BACKGROUND_MUSIC_PATH;
        if (fs.existsSync(bgmPath)) {
            command = command.input(bgmPath);
            command = command.complexFilter([
                // Zoompan filter for each image is complex to do via fluent-ffmpeg in a concat loop
                // For simplicity in this port, we do a basic slideshow first
                // If the user wants the Ken Burns effect, we can implement it with a more advanced filtergraph
                '[1:a]volume=0.2[bgm]',
                '[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]'
            ]);
            command = command.map('[aout]');
        } else {
            command = command.map('0:a');
        }

        command
            .videoFilters([
                `scale=${config.VIDEO_RESOLUTION.replace('x', ':')}:force_original_aspect_ratio=decrease`,
                `pad=${config.VIDEO_RESOLUTION.replace('x', ':')}:(ow-iw)/2:(oh-ih)/2:black`,
                'fps=30'
            ])
            .videoCodec('libx264')
            .outputOptions([
                '-preset ultrafast',
                '-crf 23',
                '-pix_fmt yuv420p',
                '-shortest',
                '-movflags +faststart'
            ])
            .audioCodec('aac')
            .save(outputPath)
            .on('start', (cmd) => console.log('Running FFmpeg:', cmd))
            .on('end', () => {
                console.log(`\n✅ Video assembled at ${outputPath}`);
                fs.unlinkSync(concatPath);
                resolve(outputPath);
            })
            .on('error', (err) => {
                console.error(`\n❌ Video assembly failed: ${err.message}`);
                reject(err);
            });
    });
}

if (require.main === module) {
    assembleVideo().catch(err => process.exit(1));
}

module.exports = { assembleVideo };
