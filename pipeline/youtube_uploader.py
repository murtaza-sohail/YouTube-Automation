# pipeline/youtube_uploader.py
"""Upload the generated video to YouTube."""
import json
import os
from pathlib import Path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required for uploading
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secret_file: Path):
    """Authenticate and return the YouTube service."""
    creds = None
    token_file = Path("token.json")
    
    # Load existing token
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
        
    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not client_secret_file.exists():
                raise FileNotFoundError(f"Client secret not found at {client_secret_file}")
                
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret_file), SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        # Save token
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
    return build("youtube", "v3", credentials=creds)

def upload_video(
    video_path: Path = Path("output/final_video.mp4"),
    metadata_path: Path = Path("output/metadata.json"),
    client_secret_path: Path = Path("client_secret.json")
):
    """Upload video to YouTube."""
    if not video_path.exists():
        print(f"Video not found at {video_path}")
        return
    if not metadata_path.exists():
        print(f"Metadata not found at {metadata_path}")
        return

    # Load metadata
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
        
    title = metadata.get("title", "Motivational Video")
    description = metadata.get("description", "Daily motivation.")
    tags = metadata.get("tags", ["motivation", "inspiration"])
    
    try:
        youtube = get_authenticated_service(client_secret_path)
    except Exception as e:
        print(f"Authentication failed: {e}")
        print("Please ensure 'client_secret.json' is present in the project root.")
        return

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "private",  # Upload as private first for safety
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(
        str(video_path),
        chunksize=1024*1024,
        resumable=True,
        mimetype="video/mp4"
    )

    print(f"Uploading '{title}'...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload complete! Video ID: {response.get('id')}")
    print(f"Video Link: https://youtu.be/{response.get('id')}")

if __name__ == "__main__":
    try:
        upload_video()
    except ImportError:
        print("Google API client libraries not installed.")
        print("pip install google-auth google-auth-oauthlib google-api-python-client")
    except Exception as e:
        print(f"An error occurred: {e}")
