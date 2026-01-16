#!/usr/bin/env python3
# pipeline/shorts_seo.py
"""Generate SEO-optimized metadata for YouTube Shorts."""
import os
from openai import OpenAI
from pathlib import Path
from .config import CHATGPT_API_KEY

client = OpenAI(api_key=CHATGPT_API_KEY)

def generate_shorts_seo(
    script_path: Path = Path("output/shorts_script.txt"),
    output_path: Path = Path("output/shorts_metadata.txt")
):
    """Generate YouTube Shorts optimized title, description, and tags.
    
    Args:
        script_path: Path to the script file
        output_path: Path to save metadata
    """
    script = script_path.read_text(encoding="utf-8")
    
    prompt = f"""Based on this YouTube Shorts script about patience and gratitude, generate:

1. A catchy, engaging TITLE (max 60 characters) that will get clicks
2. An optimized DESCRIPTION with relevant hashtags (include #Shorts, #Patience, #Gratitude)
3. 10-15 relevant TAGS for YouTube SEO

Script:
{script}

Format your response as:
TITLE: [title here]

DESCRIPTION:
[description here with hashtags]

TAGS:
[comma-separated tags]
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    metadata = response.choices[0].message.content.strip()
    
    # Save metadata
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(metadata, encoding="utf-8")
    
    print(f"✓ SEO metadata saved to {output_path}")
    print("\n" + "="*60)
    print(metadata)
    print("="*60)
    
    return output_path

if __name__ == "__main__":
    generate_shorts_seo()
