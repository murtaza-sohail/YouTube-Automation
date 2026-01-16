// pipeline_js/shorts_seo.js
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const config = require('./config');

const client = new OpenAI({
    apiKey: config.CHATGPT_API_KEY,
});

async function generateShortsSeo(
    scriptPath = config.SHORTS_SCRIPT_PATH,
    outputPath = config.SHORTS_METADATA_PATH
) {
    console.log("🏷️ Generating SEO metadata (JS)...");

    if (!fs.existsSync(scriptPath)) {
        console.error("❌ Script file not found!");
        return null;
    }

    const script = fs.readFileSync(scriptPath, 'utf8');

    const prompt = `Based on this YouTube Shorts script about patience and gratitude, generate:

1. A catchy, engaging TITLE (max 60 characters) that will get clicks
2. An optimized DESCRIPTION with relevant hashtags (include #Shorts, #Patience, #Gratitude)
3. 10-15 relevant TAGS for YouTube SEO

Script:
${script}

Format your response as:
TITLE: [title here]

DESCRIPTION:
[description here with hashtags]

TAGS:
[comma-separated tags]
`;

    try {
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: prompt }],
            temperature: 0.7,
            max_tokens: 500
        });

        const metadata = response.choices[0].message.content.trim();

        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(outputPath, metadata, 'utf8');

        console.log(`✓ SEO metadata saved to ${outputPath}`);
        console.log("\n" + "=".repeat(60));
        console.log(metadata);
        console.log("=".repeat(60));

        return outputPath;
    } catch (error) {
        console.error("❌ Error generating SEO:", error.message);
        throw error;
    }
}

if (require.main === module) {
    generateShortsSeo().catch(err => process.exit(1));
}

module.exports = { generateShortsSeo };
