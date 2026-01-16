// pipeline_js/shorts_voice_generator.js
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const config = require('./config');

const VOICE = "en-US-GuyNeural";

async function generateShortsVoice(
    scriptPath = config.SHORTS_SCRIPT_PATH,
    outputPath = config.SHORTS_AUDIO_PATH
) {
    console.log("🎙️ Generating male voice narration...");
    console.log(`  Voice: ${VOICE}`);

    const script = fs.readFileSync(scriptPath, 'utf8');
    const tempMp3 = path.join(path.dirname(outputPath), "temp_shorts_audio.mp3");

    // Use edge-tts CLI (since we know it's installed and works well)
    // We can also use npm 'edge-tts' if it provides a nice API, 
    // but the python one is already configured and reliable. 
    // However, to be "PURE JS", let's try to find if we can use the npm one.
    // If not, we'll use a shell command.

    return new Promise((resolve, reject) => {
        // Here we use the edge-tts command line tool
        const edgeTtsProcess = spawn('edge-tts', [
            '--text', script,
            '--voice', VOICE,
            '--rate', '-5%',
            '--write-media', tempMp3
        ]);

        edgeTtsProcess.on('close', (code) => {
            if (code !== 0) {
                return reject(new Error(`edge-tts process exited with code ${code}`));
            }

            // Convert MP3 to WAV using ffmpeg
            const ffmpegProcess = spawn('ffmpeg', [
                '-y', '-i', tempMp3,
                '-ar', '44100',
                '-ac', '2',
                outputPath
            ]);

            ffmpegProcess.on('close', (fcode) => {
                if (fcode !== 0) {
                    return reject(new Error(`ffmpeg conversion exited with code ${fcode}`));
                }

                // Clean up temp file
                fs.unlinkSync(tempMp3);

                // Get duration using ffprobe
                const ffprobeProcess = spawn('ffprobe', [
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    outputPath
                ]);

                let durationData = '';
                ffprobeProcess.stdout.on('data', (data) => {
                    durationData += data;
                });

                ffprobeProcess.on('close', (pcode) => {
                    const duration = parseFloat(durationData.trim());
                    console.log(`✓ Male voice audio generated: ${outputPath}`);
                    console.log(`  Duration: ${duration.toFixed(1)} seconds`);
                    resolve({ outputPath, duration });
                });
            });
        });
    });
}

if (require.main === module) {
    generateShortsVoice().catch(err => {
        console.error(err);
        process.exit(1);
    });
}

module.exports = { generateShortsVoice };
