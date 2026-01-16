#!/usr/bin/env python3
# pipeline/shorts_video_maker.py
"""Create vertical YouTube Shorts video (1080x1920, 9:16 aspect ratio).
Combines portrait images with audio narration.
"""
import subprocess
from pathlib import Path

def make_shorts_video(
    image_dir: Path = Path("output/shorts_images"),
    audio_path: Path = Path("output/shorts_audio.wav"),
    output_path: Path = Path("output/shorts_final.mp4")
):
    """Create a vertical YouTube Shorts video.
    
    Args:
        image_dir: Directory containing portrait images
        audio_path: Path to audio narration
        output_path: Output video file path
    """
    images = sorted(image_dir.glob("*.jpg"))
    
    if not images:
        print("❌ No images found!")
        return None
    
    if not audio_path.exists():
        print("❌ Audio file not found!")
        return None
    
    print(f"Creating YouTube Shorts video...")
    print(f"  Images: {len(images)}")
    print(f"  Audio: {audio_path}")
    
    # Get audio duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_duration = float(duration_result.stdout.strip())
    
    print(f"  Audio duration: {audio_duration:.1f} seconds")
    
    # Calculate duration per image
    duration_per_image = audio_duration / len(images)
    print(f"  Duration per image: {duration_per_image:.2f} seconds")
    
    # Create concat file for ffmpeg
    concat_file = Path("output/shorts_concat.txt")
    with open(concat_file, "w") as f:
        for img in images:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {duration_per_image:.2f}\n")
        # Repeat last image
        f.write(f"file '{images[-1].absolute()}'\n")
    
    # FFmpeg command for vertical video (1080x1920)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(audio_path),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",  # Good quality
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    print("\n🎬 Rendering vertical video (1080x1920)...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"\n✅ YouTube Shorts video ready!")
        print(f"   File: {output_path}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Format: 1080x1920 (9:16 vertical)")
        
        # Clean up concat file
        concat_file.unlink(missing_ok=True)
        
        return output_path
    else:
        print(f"\n❌ Video rendering failed!")
        print(f"Error: {result.stderr}")
        return None

if __name__ == "__main__":
    make_shorts_video()
