import os
import json
import uuid
from groq import Groq


def save_recipe_to_chromadb(recipe: dict, collection) -> bool:
    """Save recipe to ChromaDB collection."""
    try:
        collection.add(
            ids=[recipe["id"]],
            documents=[recipe["name"]],
            metadatas=[{"full_data": json.dumps(recipe)}]
        )
        print(f"✅ Saved '{recipe['name']}' to ChromaDB")
        return True
    except Exception as e:
        print(f"❌ ChromaDB save error: {e}")
        return False


def save_recipe_to_data_py(recipe: dict, filepath="Data/data.py") -> bool:
    """Append new recipe to data.py sample_recipes list."""
    try:
        ingredients_str = ",\n                ".join(
            [f'"{ing}"' for ing in recipe["ingredients"]]
        )

        instructions = recipe["instructions"].replace("\\", "\\\\").replace('"""', '\\"\\"\\"')

        recipe_block = f""",
        {{
            "id": str(uuid.uuid4()),
            "name": "{recipe['name']}",
            "cuisine": "{recipe['cuisine']}",
            "ingredients": [
                {ingredients_str}
            ],
            "instructions": \"\"\"{instructions}\"\"\",
            "cooking_time": "{recipe['cooking_time']}",
            "prep_time": "{recipe['prep_time']}",
            "difficulty": "{recipe['difficulty']}",
            "servings": "{recipe['servings']}",
            "calories_per_serving": "{recipe['calories_per_serving']}",
            "dietary_info": "{recipe['dietary_info']}",
            "tips": "{recipe['tips']}"
        }}"""

        with open(filepath, "r") as f:
            content = f.read()

        insert_marker = "\n    ]"
        last_index = content.rfind(insert_marker)

        if last_index == -1:
            print("❌ Could not find insert marker in data.py")
            return False

        new_content = (
            content[:last_index] +
            recipe_block +
            content[last_index:]
        )

        with open(filepath, "w") as f:
            f.write(new_content)

        print(f"✅ Saved '{recipe['name']}' to data.py")
        return True

    except Exception as e:
        print(f"❌ data.py save error: {e}")
        return False