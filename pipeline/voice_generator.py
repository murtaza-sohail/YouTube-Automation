# pipeline/voice_generator_edge.py
"""Generate audio narration using Microsoft Edge TTS.
Provides high-quality, realistic voices for free.
"""
import asyncio
import edge_tts
from pathlib import Path

# Deep, authoritative male voices - choose the best one
# Deep, authoritative female voice
VOICE = "en-US-AriaNeural"  # Professional female voice
# Alternative voices:
# "en-US-DavisNeural" - Calm, authoritative
# "en-GB-RyanNeural" - British, deep
# "en-US-EricNeural" - Deep, dramatic

async def generate_voice_async(script_path: Path = Path("output/script.txt"), output_path: Path = Path("output/audio.wav")):
    """Convert script to speech using Edge TTS and save as WAV.
    Args:
        script_path: Path to the script text file.
        output_path: Destination for the generated audio.
    """
    script = script_path.read_text(encoding="utf-8")
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate speech using Edge TTS
    communicate = edge_tts.Communicate(
        text=script,
        voice=VOICE,
        rate="-15%",  # Slow down by 15% for dramatic effect
        pitch="-5Hz"  # Slightly lower pitch for more authority
    )
    
    # Save directly as MP3 first
    temp_mp3 = output_path.parent / "temp_audio.mp3"
    await communicate.save(str(temp_mp3))
    
    # Convert MP3 to WAV using ffmpeg
    import subprocess
    cmd = [
        "ffmpeg", "-y", "-i", str(temp_mp3),
        "-ar", "44100",  # Sample rate
        "-ac", "2",  # Stereo
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Clean up temp file
    temp_mp3.unlink()
    
    print(f"✓ High-quality audio generated: {output_path}")

def generate_voice(script_path: Path = Path("output/script.txt"), output_path: Path = Path("output/audio.wav")):
    """Synchronous wrapper for the async function."""
    asyncio.run(generate_voice_async(script_path, output_path))

if __name__ == "__main__":
    generate_voice()
