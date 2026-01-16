#!/usr/bin/env python3
# pipeline/pinterest_style_fetcher.py
"""Fetch Pinterest-style images from Pexels for YouTube Shorts.
Focus on patience and gratitude themed images in portrait orientation.
"""
import os
import requests
from pathlib import Path
from .config import PEXELS_API_KEY

API_URL = "https://api.pexels.com/v1/search"

def fetch_shorts_images(output_dir: Path = Path("output/shorts_images"), num_images=20):
    """Download portrait-oriented images for YouTube Shorts.
    
    Args:
        output_dir (Path): Directory to save images.
        num_images (int): Total number of images to fetch (default: 20).
    """
    # Keywords related to patience and gratitude
    keywords = [
        "meditation peaceful",
        "gratitude journal",
        "mindfulness nature",
        "peaceful morning",
        "thankful sunset",
        "calm ocean",
        "serene forest",
        "peaceful garden",
        "grateful hands",
        "meditation sunrise",
        "peaceful lake",
        "thankful prayer",
        "calm mountains",
        "peaceful flowers",
        "gratitude heart",
        "mindful breathing",
        "peaceful sky",
        "thankful smile",
        "calm waterfall",
        "peaceful candle"
    ]
    
    headers = {"Authorization": PEXELS_API_KEY}
    output_dir.mkdir(parents=True, exist_ok=True)
    
    img_index = 1
    images_per_keyword = max(1, num_images // len(keywords))
    
    print(f"Fetching {num_images} portrait images for YouTube Shorts...")
    
    for kw in keywords:
        if img_index > num_images:
            break
            
        params = {
            "query": kw,
            "orientation": "portrait",  # Portrait for vertical video
            "size": "large",
            "per_page": images_per_keyword
        }
        
        try:
            resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            for photo in data.get("photos", []):
                if img_index > num_images:
                    break
                    
                # Get portrait image
                img_url = photo["src"]["portrait"]
                img_data = requests.get(img_url, timeout=10).content
                img_path = output_dir / f"img_{img_index:04d}.jpg"
                img_path.write_bytes(img_data)
                print(f"  ✓ Saved {img_path.name} ({kw})")
                img_index += 1
                
        except Exception as e:
            print(f"  ⚠ Warning: Failed to fetch '{kw}': {e}")
            continue
    
    total_downloaded = img_index - 1
    print(f"\n✓ Downloaded {total_downloaded} images to {output_dir}")
    return output_dir

if __name__ == "__main__":
    fetch_shorts_images()
