# pipeline/long_audio_builder.py
"""Build a 20-minute audio compilation from the core script."""
import asyncio
import edge_tts
from pathlib import Path
import subprocess

async def generate_segment(text, voice, rate, pitch, output_path):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))

async def build_long_audio():
    script_path = Path("output/script.txt")
    script = script_path.read_text(encoding="utf-8")
    
    # Define segments for the 20-minute compilation
    # 20 mins = 1200 seconds. 
    # Current script at -15% rate is ~11 mins. 
    # We need about 2 runs with different pacing or more content.
    
    segments = [
        # Part 1: Original - Deep & Slow (Intro)
        {"text": script, "rate": "-15%", "pitch": "-5Hz", "name": "part1.mp3"},
        # Part 2: Deeper & Slower (Deep Dive)
        {"text": script, "rate": "-20%", "pitch": "-10Hz", "name": "part2.mp3"},
        # Part 3: Faster & High Intensity (Peak)
        {"text": "WAKE UP. LOCK IN. THE WORLD IS WAITING. \n" + script, "rate": "+0%", "pitch": "+0Hz", "name": "part3.mp3"},
    ]
    
    temp_files = []
    print("Generating audio segments...")
    for seg in segments:
        path = Path(f"output/{seg['name']}")
        await generate_segment(seg['text'], "en-US-GuyNeural", seg['rate'], seg['pitch'], path)
        temp_files.append(path)
        print(f"✓ Generated {seg['name']}")

    # Combine using FFmpeg
    # We want exactly ~20 minutes. 
    # Part 1: ~11 mins
    # Part 2: ~13 mins
    # Total would be 24 mins. We can trim it or just take what we need.
    
    concat_list = Path("output/audio_concat.txt")
    with open(concat_list, "w") as f:
        for tf in temp_files:
            f.write(f"file '{tf.name}'\n")

    output_wav = Path("output/audio.wav")
    print("Combining segments and trimming to 20 minutes (1200s)...")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-t", "1200",  # Limit to 20 minutes
        "-ar", "44100", "-ac", "2", str(output_wav)
    ]
    subprocess.run(cmd, check=True)
    
    # Cleanup
    concat_list.unlink()
    for tf in temp_files:
        tf.unlink()
        
    print(f"✓ Final 20-minute audio built: {output_wav}")

if __name__ == "__main__":
    asyncio.run(build_long_audio())
