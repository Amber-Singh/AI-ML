import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_nutrition_from_groq(recipe_name: str, ingredients: list) -> dict:
    """Use Groq to estimate nutrition info from recipe ingredients."""
    
    ingredients_text = "\n".join(ingredients)
    
    prompt = f"""
You are a certified nutrition expert. Estimate accurate nutrition facts per serving for this recipe.

Recipe: {recipe_name}
Ingredients:
{ingredients_text}

Respond ONLY with a valid JSON object. No explanation, no markdown, no backticks.
Use exactly this format:
{{
  "calories": 420,
  "protein_g": 35,
  "carbs_g": 30,
  "fat_g": 15,
  "fiber_g": 4,
  "sugar_g": 8,
  "sodium_mg": 620
}}
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ current and free,
        messages=[{"role": "user", "content": prompt}],
        temperature=2.0,  # Higher temp for more creative estimates
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Strip markdown fences if Groq adds them
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    return json.loads(raw)