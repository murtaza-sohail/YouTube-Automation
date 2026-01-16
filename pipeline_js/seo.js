// pipeline_js/seo.js
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const config = require('./config');

const client = new OpenAI({
    apiKey: config.CHATGPT_API_KEY,
});

async function generateSeo(
    scriptPath = path.join(config.OUTPUT_DIR, "script.txt"),
    outputPath = path.join(config.OUTPUT_DIR, "metadata.txt")
) {
    console.log("🏷️ Generating SEO metadata (JS)...");

    if (!fs.existsSync(scriptPath)) {
        console.error("❌ Script file not found!");
        return null;
    }

    const script = fs.readFileSync(scriptPath, 'utf8');

    const prompt = `Generate highly optimized SEO metadata for a motivational YouTube video based on this script.

Script Summary:
${script.substring(0, 2000)}...

Provide:
1. Five high-CTR TITLES (max 70 chars)
2. One deep, emotional DESCRIPTION (include keywords, timestamps placeholder, and call-to-actions)
3. 20-30 TAGS categorized by impact

Format your response as valid JSON:
{
  "titles": ["", ""],
  "description": "",
  "tags": ""
}
`;

    try {
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: prompt }],
            temperature: 0.7,
            max_tokens: 1500,
            response_format: { type: "json_object" }
        });

        const metadata = response.choices[0].message.content.trim();

        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(outputPath, metadata, 'utf8');
        console.log(`✓ SEO metadata saved to ${outputPath}`);
        return outputPath;
    } catch (error) {
        console.error("❌ Error generating SEO:", error.message);
        throw error;
    }
}

if (require.main === module) {
    generateSeo().catch(err => process.exit(1));
}

module.exports = { generateSeo };
