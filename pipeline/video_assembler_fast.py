# pipeline/video_assembler_fast.py
"""Fast video assembly - optimized for speed."""
import subprocess
from pathlib import Path

def assemble_video_fast(
    image_dir: Path = Path("output/images"),
    audio_path: Path = Path("output/audio.wav"),
    output_path: Path = Path("output/final_video.mp4"),
):
    """Create video quickly with minimal processing."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    images = sorted(image_dir.glob("*.jpg"))
    if not images:
        raise RuntimeError(f"No images found in {image_dir}")
    
    # Create a simple concat file for ffmpeg
    concat_file = output_path.parent / "concat.txt"
    with open(concat_file, "w") as f:
        for img in images:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration 9\n")
        # Repeat last image
        f.write(f"file '{images[-1].absolute()}'\n")
    
    # Fast ffmpeg command - no complex filters, just slideshow
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "veryfast",  # Much faster encoding
        "-pix_fmt", "yuv420p",
        "-crf", "23",  # Slightly lower quality for speed
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    print("🚀 Fast rendering started...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    concat_file.unlink()
    print(f"✓ Video created: {output_path}")

if __name__ == "__main__":
    assemble_video_fast()
