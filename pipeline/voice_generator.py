# pipeline/voice_generator.py
"""Generate audio narration using ElevenLabs TTS.
Converts the full script into a single WAV file.
"""
import os
import requests
from pathlib import Path
from .config import ELEVENLABS_API_KEY

API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

def generate_voice(script_path: Path = Path("output/script.txt"), output_path: Path = Path("output/audio.wav")):
    """Send script to ElevenLabs and save the resulting audio.
    Args:
        script_path: Path to the script text file.
        output_path: Destination for the generated audio.
    """
    script = script_path.read_text(encoding="utf-8")
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    json_payload = {
        "text": script,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75,
        },
        "model_id": "eleven_monolingual_v1",
    }
    response = requests.post(f"{API_URL}/21m00Tcm4TlvDq8ikWAM/stream", headers=headers, json=json_payload, stream=True)
    # Voice ID: Rachel (American, calm, deep female)
    response.raise_for_status()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    generate_voice()
