# pipeline/script_expander.py
"""Expand the provided motivational text to reach 20 minutes."""
from pathlib import Path
from openai import OpenAI
from .config import CHATGPT_API_KEY

client = OpenAI(api_key=CHATGPT_API_KEY)

CORE_TEXT = Path("output/script.txt").read_text(encoding="utf-8")

PROMPT = f"""
You are an expert motivational script writer. I have a core message that needs to be expanded into a 20-minute cinematic script (approx 2400-2600 words).
The tone must be: BRUTAL, STOIC, DARK, and EMPOWERING.

Core Message:
{CORE_TEXT}

Instructions:
1. Use the core message as the foundation. Start with it.
2. Expand on each point with visceral, psychological depth.
3. Add new sections focusing on:
   - The psychology of solitude.
   - The physics of momentum vs laziness.
   - The concept of "Internal Sovereignty" (not being a slave to feelings).
   - The anatomy of a "Relentless Mindset".
   - The cold reality of mortality.
4. Keep the language simple, punchy, and rhythmic. No fluff, no clichés like "reach for the stars".
5. Target word count: 2500 words.
6. Format as plain text. No stage directions or emojis.
"""

def expand_script(output_path: Path = Path("output/script_long.txt")):
    print("Expanding script to 20 minutes...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": PROMPT}],
        temperature=0.7,
        max_tokens=4000,
    )
    long_script = response.choices[0].message.content.strip()
    output_path.write_text(long_script, encoding="utf-8")
    print(f"✓ Long script saved to {output_path}")

if __name__ == "__main__":
    expand_script()
