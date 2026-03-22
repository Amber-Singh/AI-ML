from Data.data import sample_recipes
import json 
import os
from groq import Groq



_recipes_collection = None
_recipes_cache = None

def init_chromadb():
    """Initialize ChromaDB with recipes - no embeddings"""
    global _recipes_collection, _recipes_cache
    
    if _recipes_collection is not None:
        return _recipes_collection
    
    try:
        import chromadb
        
        # Use ephemeral client (in-memory, no embeddings)
        client = chromadb.EphemeralClient()
        _recipes_collection = client.get_or_create_collection(name="recipes")
        
        # Add recipes without embeddings
        ids = [str(i) for i in range(len(sample_recipes))]
        documents = [recipe['name'] for recipe in sample_recipes]
        metadatas = [{"full_data": json.dumps(recipe)} for recipe in sample_recipes]
        
        try:
            _recipes_collection.add(ids=ids, documents=documents, metadatas=metadatas)
            print(f"Added {len(ids)} recipes to ChromaDB")
        except Exception as e:
            print(f"Error adding to ChromaDB: {e}, using cache")
            _recipes_cache = sample_recipes
        
        return _recipes_collection
    except Exception as e:
        print(f"ChromaDB init error: {e}")
        _recipes_cache = sample_recipes
        return None

def get_recipes():
    """Fetch all recipes from ChromaDB or cache"""
    try:
        collection = init_chromadb()
        if collection and _recipes_cache is None:
            result = collection.get()
            if result and result['metadatas']:
                return [json.loads(m['full_data']) for m in result['metadatas']]
    except Exception as e:
        print(f"Error fetching from ChromaDB: {e}")
    
    # Use cache if ChromaDB fails
    if _recipes_cache:
        return _recipes_cache
    return sample_recipes


def extract_keywords(query: str) -> list:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
        You are a recipe search assistant. Extract the MOST SPECIFIC recipe name or ingredients from the query.
        Return ONLY a JSON array. No explanation, no markdown, no backticks.

        Rules:
        - Prefer full recipe name over individual words
        - If user asks for a specific dish, return that exact dish name as first keyword
        - Only split into individual words if no specific dish is mentioned

        Query: "{query}"

        Examples:
        Input: "recipe for Thai Green Curry"
        Output: ["thai green curry"]

        Input: "I want something spicy with chicken"
        Output: ["spicy", "chicken"]

        Input: "please tell me how to make Pad Thai"
        Output: ["pad thai"]

        Input: "something with tomatoes and cheese"
        Output: ["tomatoes", "cheese"]
        """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)

def get_collection():
    """Return ChromaDB collection for external use."""
    return init_chromadb()

def search_recipes(query):
    """Search recipes using Groq keyword extraction + flexible matching."""
    try:
        recipes = get_recipes()
        query_lower = query.lower()
        matching = []

        # Step 1 — Try direct match first (fast)
        for recipe in recipes:
            if query_lower in recipe['name'].lower():
                matching.append(recipe)
            elif any(query_lower in ing.lower() for ing in recipe.get('ingredients', [])):
                matching.append(recipe)

        # Step 2 — If no direct match, use Groq to extract keywords
        if not matching:
            print(f"No direct match, extracting keywords with Groq...")
            keywords = extract_keywords(query)
            print(f"Extracted keywords: {keywords}")

            for recipe in recipes:
                recipe_text = (
                    recipe['name'].lower() + " " +
                    " ".join(recipe.get('ingredients', [])).lower() + " " +
                    recipe.get('cuisine', '').lower()
                )
                
                # Check full phrase first (most specific)
                full_phrase = keywords[0].lower() if keywords else ""
                if full_phrase and full_phrase in recipe_text:
                    if recipe not in matching:
                        matching.append(recipe)
                # Only fall back to individual keywords if no full phrase match found
                elif not full_phrase and any(kw.lower() in recipe_text for kw in keywords):
                    if recipe not in matching:
                        matching.append(recipe)

        print(f"Found {len(matching)} recipes matching '{query}'")
        return matching

    except Exception as e:
        print(f"Error searching: {e}")
        return []
    
   