#!/usr/bin/env python3
# pipeline/shorts_script_generator.py
"""Generate a short motivational script for YouTube Shorts (60 seconds).
Focus on patience and gratitude with simple, clear English.
"""
import os
from openai import OpenAI
from pathlib import Path

# Load API key from config or environment
from .config import CHATGPT_API_KEY

client = OpenAI(api_key=CHATGPT_API_KEY)

PROMPT = """
Write a motivational script for a 60-second YouTube Shorts video about PATIENCE and GRATITUDE.

Requirements:
- Use SIMPLE, CLEAR English (easy to understand)
- Approximately 150-180 words (speaking pace: ~150 words/minute)
- Calm, peaceful, and uplifting tone
- Focus on the power of patience and gratitude in daily life
- Make it relatable and inspiring
- No complex vocabulary or long sentences
- Start with a strong hook to grab attention in first 3 seconds

Structure:
1. Hook (3-5 seconds): Powerful opening question or statement
2. Main message (45 seconds): Core wisdom about patience and gratitude
3. Call to action (10 seconds): Encourage viewers to practice these values

Write ONLY the script text, no titles, no formatting, just the words to be spoken.
"""

def generate_shorts_script(output_path: Path = Path("output/shorts_script.txt")):
    """Generate a 60-second script about patience and gratitude."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": PROMPT}],
        temperature=0.7,
        max_tokens=300,
    )
    script = response.choices[0].message.content.strip()
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script, encoding="utf-8")
    
    # Count words
    word_count = len(script.split())
    print(f"✓ Script saved to {output_path}")
    print(f"  Word count: {word_count} words")
    print(f"  Estimated duration: ~{word_count/2.5:.0f} seconds")
    
    return output_path

if __name__ == "__main__":
    generate_shorts_script()
