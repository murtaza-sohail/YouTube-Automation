# pipeline/seo.py
"""Generate SEO-optimized metadata for the YouTube video.
Creates a click-bait title and a description with tags using OpenAI.
"""
import json
from openai import OpenAI
from pathlib import Path
from .config import CHATGPT_API_KEY

client = OpenAI(api_key=CHATGPT_API_KEY)

def generate_metadata(script_path: Path = Path("output/script.txt"), output_path: Path = Path("output/metadata.json")):
    """Read the script and generate title/description."""
    if not script_path.exists():
        print(f"Script not found at {script_path}, skipping metadata generation.")
        return

    script_excerpt = script_path.read_text(encoding="utf-8")[:1000]  # First 1000 chars for context
    
    prompt = f"""
    Based on the following motivational script excerpt, generate:
    1. A high-CTR, clickbait YouTube title (max 60 chars) specifically targeted at a US audience (American English idioms, emotionally resonant).
    2. An SEO-optimized video description (max 200 words) for US viewers, including keywords like #motivation, #discipline, #success.
    
    Script Excerpt:
    "{script_excerpt}..."
    
    Return the result as valid JSON with keys: "title", "description".
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
    )
    
    content = response.choices[0].message.content.strip()
    try:
        # cleanup markdown code blocks if present
        if content.startswith("```json"):
            content = content.strip("```json").strip("```")
        elif content.startswith("```"):
            content = content.strip("```")
            
        data = json.loads(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Metadata saved to {output_path}")
    except json.JSONDecodeError:
        print("Failed to parse SEO metadata JSON. Raw output:")
        print(content)

if __name__ == "__main__":
    generate_metadata()
