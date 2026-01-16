// pipeline_js/script_generator.js
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const config = require('./config');

const client = new OpenAI({
    apiKey: config.CHATGPT_API_KEY,
});

const PROMPT = `
Write a cinematic motivational script of 1800-2200 words in English.
Tone: dark → intense → empowering.
Structure:
1. Brutal cold hook (first 15 seconds).
2. Pain, failure, rejection.
3. Isolation & discipline.
4. Mental transformation.
5. Legacy-driven ending.
Use simple, brutal, real language. No emojis, clichés, or fluff.
`;

async function generateScript(outputPath = path.join(config.OUTPUT_DIR, "script.txt")) {
    console.log("📝 Generating long-form motivational script...");

    try {
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "system", content: PROMPT }],
            temperature: 0.8,
            max_tokens: 3000,
        });

        const script = response.choices[0].message.content.trim();

        // Ensure directory exists
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(outputPath, script, 'utf8');

        console.log(`✓ Script saved to ${outputPath}`);
        return outputPath;
    } catch (error) {
        console.error("❌ Error generating script:", error.message);
        throw error;
    }
}

if (require.main === module) {
    generateScript().catch(err => process.exit(1));
}

module.exports = { generateScript };
