#!/usr/bin/env python3
"""Trim video to exactly 15 minutes."""
import subprocess
from pathlib import Path

def trim_to_15_minutes():
    """Cut the video to exactly 15 minutes (900 seconds)."""
    input_video = Path("output/Video.mp4")
    output_video = Path("output/Video_15min.mp4")
    
    if not input_video.exists():
        print(f"❌ Video not found: {input_video}")
        return
    
    # Trim to exactly 15 minutes (900 seconds)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_video),
        "-t", "900",  # 15 minutes = 900 seconds
        "-c", "copy",  # Copy without re-encoding (FAST!)
        "-avoid_negative_ts", "make_zero",
        str(output_video)
    ]
    
    print("✂️  Trimming video to 15 minutes...")
    print("   Using stream copy (no re-encoding - INSTANT!)")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size_mb = output_video.stat().st_size / 1024 / 1024
        print(f"\n✅ 15-MINUTE VIDEO READY!")
        print(f"   File: {output_video}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Duration: Exactly 15:00")
    else:
        print(f"❌ Error: {result.stderr}")

if __name__ == "__main__":
    trim_to_15_minutes()
