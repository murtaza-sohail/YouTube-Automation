# pipeline/subtitle_generator.py
"""Generate animated subtitles for the video."""
import subprocess
from pathlib import Path
import re

def create_subtitles(
    script_path: Path = Path("output/script.txt"),
    audio_path: Path = Path("output/audio.wav"),
    output_path: Path = Path("output/subtitles.srt")
):
    """Create SRT subtitle file with word-level timing."""
    
    # Read script
    script = script_path.read_text(encoding="utf-8")
    
    # Get audio duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    
    # Split script into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', script) if s.strip()]
    
    # For the 20-minute compilation, the script is spoken twice (Part 1 and Part 2)
    # We will double the sentences to match the audio
    full_sentences = sentences + sentences
    
    # Calculate timing per sentence
    time_per_sentence = duration / len(full_sentences)
    
    # Create SRT content
    srt_content = []
    current_time = 0
    
    for i, sentence in enumerate(full_sentences, 1):
        start_time = current_time
        end_time = current_time + time_per_sentence
        
        # Format timestamps (SRT format: HH:MM:SS,mmm)
        start_str = format_timestamp(start_time)
        end_str = format_timestamp(end_time)
        
        # Add subtitle entry
        srt_content.append(f"{i}")
        srt_content.append(f"{start_str} --> {end_str}")
        srt_content.append(sentence.upper())  # Uppercase for impact
        srt_content.append("")  # Blank line
        
        current_time = end_time
    
    # Write SRT file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(srt_content), encoding="utf-8")
    
    print(f"✓ Subtitles created: {output_path}")
    return output_path

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def add_subtitles_to_video(
    video_path: Path = Path("output/final_video.mp4"),
    subtitle_path: Path = Path("output/subtitles.srt"),
    output_path: Path = Path("output/final_video_subtitled.mp4")
):
    """Add animated subtitles to video using ffmpeg."""
    
    # Create subtitle style with animations
    subtitle_style = (
        "FontName=Impact,"
        "FontSize=32,"
        "PrimaryColour=&H00FFFFFF,"  # White text
        "OutlineColour=&H00000000,"  # Black outline
        "BackColour=&H80000000,"     # Semi-transparent background
        "Bold=1,"
        "Outline=3,"
        "Shadow=2,"
        "Alignment=2"  # Bottom center
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={subtitle_path}:force_style='{subtitle_style}'",
        "-c:a", "copy",  # Copy audio without re-encoding
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        str(output_path)
    ]
    
    print("🎬 Adding animated subtitles...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    print(f"✓ Subtitled video created: {output_path}")
    return output_path

if __name__ == "__main__":
    # Generate subtitles
    srt_path = create_subtitles()
    
    # Add to video
    add_subtitles_to_video(subtitle_path=srt_path)
