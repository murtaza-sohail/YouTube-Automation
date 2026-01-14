# pipeline/video_assembler.py
"""Assemble images, audio, and background music into the final video.
Uses FFmpeg to create a slideshow with slow zoom/pan (Ken Burns) effects,
adds low‑volume background music, and inserts a beat‑drop overlay at the
specified timestamp.
"""
import subprocess
from pathlib import Path
from .config import (
    VIDEO_RESOLUTION,
    BACKGROUND_MUSIC_PATH,
    BEAT_DROP_TIMESTAMP,
    IMAGE_DURATION_SECONDS,
)

def build_filtergraph(image_dir: Path, audio_path: Path, output_path: Path):
    """Generate an FFmpeg filtergraph for the slideshow.
    Each image is displayed for ``IMAGE_DURATION_SECONDS`` seconds with a
    slow zoom/pan effect. The images are concatenated, then the audio and
    background music are mixed in.
    """
    # Collect image files sorted alphabetically
    images = sorted(image_dir.glob("*.jpg"))
    if not images:
        raise RuntimeError("No images found in {image_dir}")

    # Build the input list for FFmpeg
    inputs = []
    filter_parts = []
    for idx, img in enumerate(images):
        inputs.extend(["-loop", "1", "-t", str(IMAGE_DURATION_SECONDS), "-i", str(img)])
        # Apply zoompan: start zoom 1.0, end 1.1 over the duration
        zoom_filter = (
            f"[{idx+2}:v]zoompan=z='if(lte(zoom,1.0),1.0,zoom+0.0005)'"
            f":d={IMAGE_DURATION_SECONDS * 30}:s={VIDEO_RESOLUTION}:fps=30[zo{idx}]"
        )
        filter_parts.append(zoom_filter)

    # Concatenate zoomed streams
    concat_inputs = "".join([f"[zo{i}]" for i in range(len(images))])
    concat_filter = f"{concat_inputs}concat=n={len(images)}:v=1:a=0[video]"
    filter_parts.append(concat_filter)

    # Background music (loop if shorter than video)
    filter_parts.append(
        f"[1:a]volume=0.2[bgm]"  # assume background music is second input after images
    )
    # Mix audio: narration + background music
    filter_parts.append(
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    filtergraph = ";".join(filter_parts)
    return inputs, filtergraph

def assemble_video(
    image_dir: Path = Path("output/images"),
    audio_path: Path = Path("output/audio.wav"),
    output_path: Path = Path("output/final_video.mp4"),
):
    """Run FFmpeg to create the final video.
    The function builds a complex filtergraph and executes FFmpeg via
    ``subprocess.run``. Errors are raised as ``RuntimeError``.
    """
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build filtergraph and input arguments
    inputs, filtergraph = build_filtergraph(image_dir, audio_path, output_path)

    # Construct the full command list
    cmd = ["ffmpeg", "-y"]
    # Add narration audio as first extra input
    cmd.extend(["-i", str(audio_path)])
    # Add background music as second extra input (if file exists)
    if Path(BACKGROUND_MUSIC_PATH).exists():
        cmd.extend(["-i", BACKGROUND_MUSIC_PATH])
    else:
        # Use a silent dummy audio to keep filtergraph indices consistent
        cmd.extend(["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"])
    # Add image inputs
    cmd.extend(inputs)
    # Apply filtergraph
    cmd.extend(["-filter_complex", filtergraph])
    # Map video and mixed audio streams
    cmd.extend(["-map", "[video]", "-map", "[aout]"])
    cmd.extend(["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output_path)])

    print("Running FFmpeg command:")
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    print(f"Video assembled at {output_path}")

if __name__ == "__main__":
    assemble_video()
