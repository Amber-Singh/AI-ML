from crewai import Task

def create_research_tasks(researcher, nutritionist, formatter, query: str):
    
    # Task 1 — Research the recipe
    research_task = Task(
        description=f"""
        Research a complete and authentic recipe for: {query}
        
        Find and provide:
        - Full recipe name
        - Cuisine type
        - Complete ingredient list with exact measurements
        - Step by step cooking instructions
        - Prep time and cooking time
        - Difficulty level (Easy/Medium/Hard)
        - Number of servings
        - Any special cooking tips
        
        Be thorough and accurate. Use your culinary knowledge to provide
        the most authentic version of this recipe.
        """,
        expected_output="Complete recipe with all details including ingredients, instructions, times and tips",
        agent=researcher
    )

    # Task 2 — Analyse nutrition
    nutrition_task = Task(
        description=f"""
        Based on the recipe researched for {query}, analyse the nutrition.
        
        Provide:
        - Estimated calories per serving
        - Protein (grams)
        - Carbohydrates (grams)  
        - Fats (grams)
        - Dietary information (Contains dairy/gluten/nuts etc)
        - Whether it is vegan/vegetarian/gluten-free
        
        Use the ingredient quantities from the research to make accurate estimates.
        """,
        expected_output="Detailed nutrition analysis with calories, macros and dietary information",
        agent=nutritionist,
        context=[research_task]  # Gets research output as context
    )

    # Task 3 — Format everything into JSON
    format_task = Task(
        description=f"""
        Take the recipe research and nutrition analysis for {query} and format 
        it into a structured JSON object.
        
        Return ONLY a valid JSON object, no explanation, no markdown, no backticks.
        
        Use EXACTLY this format:
        {{
            "name": "Recipe Name",
            "cuisine": "Indian/Italian/etc",
            "ingredients": [
                "ingredient 1 with quantity",
                "ingredient 2 with quantity"
            ],
            "instructions": "1. Step one\\n2. Step two\\n3. Step three",
            "cooking_time": "25 minutes",
            "prep_time": "20 minutes",
            "difficulty": "Easy/Medium/Hard",
            "servings": "4",
            "calories_per_serving": "420",
            "dietary_info": "Contains dairy. Gluten-free without naan.",
            "tips": "Pro tips here"
        }}
        
        Rules:
        - ingredients MUST be a JSON array of strings
        - instructions MUST be a single string with numbered steps
        - difficulty MUST be one of: Easy, Medium, Hard
        - cooking_time and prep_time MUST include "minutes" or "hours"
        - calories_per_serving MUST be a string number e.g. "420"
        - servings MUST be a string number e.g. "4"
        - Return ONLY the JSON, nothing else
        """,
        expected_output="A valid JSON object with all recipe fields correctly filled",
        agent=formatter,
        context=[research_task, nutrition_task]  # Gets both outputs as context
    )

    return [research_task, nutrition_task, format_task]