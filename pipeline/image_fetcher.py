# pipeline/image_fetcher.py
"""Fetch cinematic images from Pexels based on keywords.
Each image corresponds to a segment of the narration (≈9 seconds).
"""
import os
import requests
from pathlib import Path
from .config import PEXELS_API_KEY, IMAGE_DURATION_SECONDS

API_URL = "https://api.pexels.com/v1/search"

def fetch_images(keywords, output_dir: Path = Path("output/images"), per_keyword=1):
    """Download images for each keyword.
    Args:
        keywords (list[str]): List of search terms.
        output_dir (Path): Directory to save images.
        per_keyword (int): Number of images to fetch per keyword.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    output_dir.mkdir(parents=True, exist_ok=True)
    img_index = 1
    for kw in keywords:
        params = {"query": kw, "orientation": "landscape", "size": "large", "per_page": per_keyword}
        resp = requests.get(API_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        for photo in data.get("photos", []):
            img_url = photo["src"]["large2x"]
            img_data = requests.get(img_url).content
            img_path = output_dir / f"img_{img_index:04d}.jpg"
            img_path.write_bytes(img_data)
            print(f"Saved {img_path}")
            img_index += 1
    return output_dir

if __name__ == "__main__":
    # Extensive keyword list for 20-minute video (~400 images)
    kw_list = [
        "discipline gym", "dark room", "lonely man", "rain night city", "focus hard work",
        "clock ticking", "mountain peak", "running rain", "boxing training", "shadow boxing",
        "cold morning", "empty street night", "man in suit silhouette", "library studying", "chess player",
        "wolf howling", "eagle soaring", "lion roar", "stormy ocean", "burning fire",
        "ancient ruins", "modern office night", "sweat workout", "heavy weights", "tired face",
        "sunrise mountain", "stargazing", "bridge in fog", "forest mist", "desert road",
        "climbing rock", "lifting heavy", "underwater swimming", "fast car driving night", "city lights blur",
        "meditation", "praying", "writing journal", "drawing plans", "building structure",
        "gears turning", "compass", "map adventure", "climbing stairs", "tunnel light",
        "rain on window", "puddle reflection", "lightning storm", "snow mountain", "volcano lava",
        "old tree", "new sprout", "breaking chains", "wall breaking", "door opening",
        "clenched fist", "intense eyes", "staring mirror", "walking alone", "standing tall",
        "black and white portrait", "cinematic lighting", "gritty texture", "industrial site", "construction",
        "space nebula", "planet earth", "sunrise from space", "satellite", "rocket launch",
        "running track", "olympic stadium", "crowd cheering blur", "trophy", "medal",
        "sweeping floor", "washing dishes", "simple lifestyle", "asceticism", "stoicism",
        "fighting", "defense", "guards", "armor", "sword", "shield", "throne", "crown"
    ]
    # Fetch 5 images per keyword = 80 * 5 = 400 images
    fetch_images(kw_list, per_keyword=5)
