#!/usr/bin/env python3
# pipeline/shorts_voice_generator.py
"""Generate male voice narration for YouTube Shorts using Microsoft Edge TTS."""
import asyncio
import edge_tts
from pathlib import Path

# Male voices - calm and clear for patience/gratitude theme
VOICE = "en-US-GuyNeural"  # Calm, warm male voice
# Alternative voices:
# "en-US-DavisNeural" - Calm, authoritative
# "en-GB-RyanNeural" - British, deep
# "en-US-EricNeural" - Deep, dramatic

async def generate_shorts_voice_async(
    script_path: Path = Path("output/shorts_script.txt"),
    output_path: Path = Path("output/shorts_audio.wav")
):
    """Convert script to speech using Edge TTS with male voice.
    
    Args:
        script_path: Path to the script text file.
        output_path: Destination for the generated audio.
    """
    script = script_path.read_text(encoding="utf-8")
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating male voice narration...")
    print(f"  Voice: {VOICE}")
    
    # Generate speech using Edge TTS
    communicate = edge_tts.Communicate(
        text=script,
        voice=VOICE,
        rate="-5%",  # Slightly slower for clarity
        pitch="+0Hz"  # Natural pitch
    )
    
    # Save directly as MP3 first
    temp_mp3 = output_path.parent / "temp_shorts_audio.mp3"
    await communicate.save(str(temp_mp3))
    
    # Convert MP3 to WAV using ffmpeg
    import subprocess
    cmd = [
        "ffmpeg", "-y", "-i", str(temp_mp3),
        "-ar", "44100",  # Sample rate
        "-ac", "2",  # Stereo
        str(output_path)
    ]
    
    result = subprocess.run(cmd, check=True, capture_output=True)
    
    # Clean up temp file
    temp_mp3.unlink()
    
    # Get audio duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(output_path)
    ]
    duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    duration = float(duration_result.stdout.strip())
    
    print(f"✓ Male voice audio generated: {output_path}")
    print(f"  Duration: {duration:.1f} seconds")
    
    return output_path, duration

def generate_shorts_voice(
    script_path: Path = Path("output/shorts_script.txt"),
    output_path: Path = Path("output/shorts_audio.wav")
):
    """Synchronous wrapper for the async function."""
    return asyncio.run(generate_shorts_voice_async(script_path, output_path))

if __name__ == "__main__":
    generate_shorts_voice()
