import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_recipe(recipe: dict, target_language: str) -> dict:
    """Translate full recipe to target language using Groq."""
    
    prompt = f"""
You are a professional translator. Translate the following recipe details into {target_language}.

Recipe Name: {recipe['name']}

Ingredients:
{chr(10).join(recipe['ingredients'])}

Instructions:
{recipe['instructions']}

Tips:
{recipe.get('tips', '')}

Respond ONLY with a valid JSON object. No explanation, no markdown, no backticks.
Use exactly this format:
{{
  "name": "translated recipe name",
  "ingredients": ["translated ingredient 1", "translated ingredient 2"],
  "instructions": "translated instructions",
  "tips": "translated tips"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if Groq adds them
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)