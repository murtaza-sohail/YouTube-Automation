// pipeline_js/shorts_script_generator.js
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const config = require('./config');

const client = new OpenAI({
    apiKey: config.CHATGPT_API_KEY,
});

const PROMPT = `
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
`;

async function generateShortsScript(outputPath = config.SHORTS_SCRIPT_PATH) {
    console.log("📝 Generating shorts script...");

    try {
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "system", content: PROMPT }],
            temperature: 0.7,
            max_tokens: 300,
        });

        const script = response.choices[0].message.content.trim();

        // Ensure directory exists
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(outputPath, script, 'utf8');

        const wordCount = script.split(/\s+/).length;
        console.log(`✓ Script saved to ${outputPath}`);
        console.log(`  Word count: ${wordCount} words`);
        console.log(`  Estimated duration: ~${Math.round(wordCount / 2.5)} seconds`);

        return outputPath;
    } catch (error) {
        console.error("❌ Error generating script:", error.message);
        throw error;
    }
}

if (require.main === module) {
    generateShortsScript().catch(err => process.exit(1));
}

module.exports = { generateShortsScript };
