#!/usr/bin/env python3
"""Ultra-fast video maker - uses only first 10 images for speed."""
import subprocess
from pathlib import Path

def make_video_ultrafast():
    """Create video FAST - only use 10 images, repeat them."""
    image_dir = Path("output/images")
    audio_path = Path("output/audio.wav")
    output_path = Path("output/final_video.mp4")
    
    images = sorted(image_dir.glob("*.jpg"))  # USE ALL IMAGES!
    
    if not images:
        print("❌ No images found!")
        return
    
    print(f"✓ Using {len(images)} images (ALL unique)")
    print(f"✓ Audio: {audio_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Calculate duration per image to match audio
    audio_duration = 1943.64  # ~32 minutes
    duration_per_image = audio_duration / len(images)
    
    # Create concat file - use each image once
    concat_file = Path("output/concat_ultra.txt")
    with open(concat_file, "w") as f:
        for img in images:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {duration_per_image:.2f}\n")
        f.write(f"file '{images[-1].absolute()}'\n")
    
    # Ultra-fast ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "ultrafast",  # FASTEST preset
        "-tune", "stillimage",   # Optimized for still images
        "-pix_fmt", "yuv420p",
        "-crf", "28",  # Lower quality = faster
        "-vf", "scale=1280:720,fps=15",  # Lower res, lower fps = MUCH faster
        "-c:a", "aac",
        "-b:a", "96k",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    print("🚀 Starting ULTRA-FAST render...")
    print("   (720p, 15fps, ultrafast preset)")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"\n✅ VIDEO READY: {output_path}")
        print(f"   Size: {size_mb:.1f} MB")
    else:
        print(f"❌ Failed!")
    
    concat_file.unlink(missing_ok=True)

if __name__ == "__main__":
    make_video_ultrafast()
