# pipeline/voice_generator_gtts.py
"""Generate audio narration using Google Text-to-Speech (gTTS).
Converts the full script into a single WAV file.
"""
import os
import subprocess
from pathlib import Path
from gtts import gTTS

def generate_voice(script_path: Path = Path("output/script.txt"), output_path: Path = Path("output/audio.wav")):
    """Convert script to speech using gTTS and save as WAV.
    Args:
        script_path: Path to the script text file.
        output_path: Destination for the generated audio.
    """
    script = script_path.read_text(encoding="utf-8")
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate speech using gTTS with slow speed for dramatic effect
    tts = gTTS(text=script, lang='en', slow=True)
    
    # Save as MP3 first (gTTS default)
    temp_mp3 = output_path.parent / "temp_audio.mp3"
    tts.save(str(temp_mp3))
    
    # Convert MP3 to WAV using ffmpeg and slow down by 10%
    cmd = [
        "ffmpeg", "-y", "-i", str(temp_mp3),
        "-filter:a", "atempo=0.9",  # Slow down by 10%
        "-ar", "44100",  # Sample rate
        "-ac", "2",  # Stereo
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # If slowing down fails, just convert without speed change
        cmd = ["ffmpeg", "-y", "-i", str(temp_mp3), "-ar", "44100", "-ac", "2", str(output_path)]
        subprocess.run(cmd, check=True)
    
    # Clean up temp file
    temp_mp3.unlink()
    
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    generate_voice()
