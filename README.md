# YouTube Automation Pipeline

This project automates the creation of motivational YouTube videos. It generates a script, fetches relevant images, creates a voiceover, assembles the video, and prepares metadata.

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for video processing.
  - *Linux*: `sudo apt install ffmpeg`
  - *Mac*: `brew install ffmpeg`
  - *Windows*: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/murtaza-sohail/YouTube-Automation.git
    cd YouTube-Automation
    ```

2.  **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

**Important**: This project uses several APIs. You must ensure your API keys are valid.

Currently, API keys are set in `run_pipeline.sh`.
> **Security Note**: Never commit real API keys to a public GitHub repository. It is recommended to use environment variables.

Required Keys:
- `PEXELS_API_KEY` (for stock footages/images)
- `CHATGPT_API_KEY` (for script generation)
- `ELEVENLABS_API_KEY` (for voiceover)

## Usage

The entire pipeline can be run using the provided shell script:

```bash
./run_pipeline.sh
```

### Steps Performed:
1.  **Script Generation**: Creates a motivational script.
2.  **Image Fetching**: Downloads visuals based on keywords.
3.  **Voiceover Generation**: Converts script to audio.
4.  **Video Assembly**: Combines audio and visuals into a video.
5.  **Metadata Generation**: Creates title, description, and tags.
6.  **Upload**: (Optional) Uploads to YouTube if configured.

## Output

All generated files (scripts, audio, video, metadata) will be stored in the `output/` directory.
