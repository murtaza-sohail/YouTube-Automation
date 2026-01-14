# pipeline/script_generator.py
"""Generate a motivational script using OpenAI's Chat Completion API.
The script length should be 1800‑2200 words and follow the specified structure.
"""
import os
import json
from openai import OpenAI
from pathlib import Path

# Load API key from config or environment
from .config import CHATGPT_API_KEY

client = OpenAI(api_key=CHATGPT_API_KEY)

PROMPT = """
Write a cinematic motivational script of 1800-2200 words in English.
Tone: dark → intense → empowering.
Structure:
1. Brutal cold hook (first 15 seconds).
2. Pain, failure, rejection.
3. Isolation & discipline.
4. Mental transformation.
5. Legacy-driven ending.
Use simple, brutal, real language. No emojis, clichés, or fluff.
"""

def generate_script(output_path: Path = Path("output/script.txt")):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": PROMPT}],
        temperature=0.8,
        max_tokens=3000,
    )
    script = response.choices[0].message.content.strip()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script, encoding="utf-8")
    print(f"Script saved to {output_path}")

if __name__ == "__main__":
    generate_script()
