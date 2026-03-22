from crewai import Task

def create_recipe_task(agent, user_requirements: str):
    task = Task(
        description=f"""
        Create a complete recipe based on these requirements:
        {user_requirements}
        
        You MUST respond with ONLY a valid JSON object, no explanation, no markdown, no backticks.
        
        Use EXACTLY this format:
        {{
            "name": "Recipe Name",
            "cuisine": "Indian/Italian/etc",
            "ingredients": [
                "ingredient 1 with quantity",
                "ingredient 2 with quantity",
                "ingredient 3 with quantity"
            ],
            "instructions": "1. Step one\\n2. Step two\\n3. Step three",
            "cooking_time": "25 minutes",
            "prep_time": "20 minutes",
            "difficulty": "Easy/Medium/Hard",
            "servings": "4",
            "calories_per_serving": "420",
            "dietary_info": "Contains dairy. Gluten-free without naan.",
            "tips": "Pro tips for best results"
        }}
        
        Rules:
        - ingredients MUST be a JSON array of strings with quantities
        - instructions MUST be a single string with numbered steps separated by \\n
        - difficulty MUST be one of: Easy, Medium, Hard
        - cooking_time and prep_time MUST include "minutes" or "hours"
        - calories_per_serving MUST be a string number e.g. "420"
        - servings MUST be a string number e.g. "4"
        - Never leave any field empty, use "Unknown" if not sure
        - Return ONLY the JSON object, nothing else
        - Use only standard ASCII characters, no special symbols like °C, é, ñ etc.
        - Write temperatures as "180C" not "180°C"
        """,
        
        expected_output="A valid JSON object with all recipe fields filled in correctly",
        
        agent=agent
    )
    
    return task