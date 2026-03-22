import json
import os
from Data.data import sample_recipes


def delete_from_data_py(recipe_names: list) -> int:
    """Permanently delete recipes from data.py by name."""
    filepath = "Data/data.py"
    deleted_count = 0

    try:
        with open(filepath, "r") as f:
            content = f.read()

        lines = content.split('\n')
        result_lines = []
        skip = False
        brace_count = 0
        current_recipe_lines = []
        in_recipe = False

        i = 0
        while i < len(lines):
            line = lines[i]

            if line.strip() == '{':
                in_recipe = True
                brace_count = 1
                current_recipe_lines = [line]
                i += 1
                continue

            if in_recipe:
                current_recipe_lines.append(line)
                brace_count += line.count('{') - line.count('}')

                if '"name":' in line:
                    for name in recipe_names:
                        if f'"{name}"' in line:
                            skip = True
                            break

                if brace_count <= 0:
                    in_recipe = False
                    if not skip:
                        result_lines.extend(current_recipe_lines)
                    else:
                        deleted_count += 1
                        print(f"✅ Removed '{[n for n in recipe_names]}' from data.py")
                    skip = False
                    current_recipe_lines = []
            else:
                result_lines.append(line)

            i += 1

        with open(filepath, "w") as f:
            f.write('\n'.join(result_lines))

        print(f"✅ Deleted {deleted_count} recipes from data.py")

    except Exception as e:
        print(f"❌ data.py delete error: {e}")

    return deleted_count


def delete_from_json(recipe_ids: list) -> int:
    """Delete custom recipes from JSON and sample recipes from data.py."""
    deleted_count = 0

    # Get sample recipe id → name mapping
    sample_id_to_name = {r["id"]: r["name"] for r in sample_recipes}

    # Separate sample vs custom
    names_to_delete_from_data = [
        sample_id_to_name[rid]
        for rid in recipe_ids
        if rid in sample_id_to_name
    ]
    custom_ids_to_delete = [
        rid for rid in recipe_ids
        if rid not in sample_id_to_name
    ]

    # Delete sample recipes from data.py permanently
    if names_to_delete_from_data:
        deleted_count += delete_from_data_py(names_to_delete_from_data)

    # Delete custom recipes from custom_recipes.json
    custom_path = "Data/custom_recipes.json"
    if custom_ids_to_delete and os.path.exists(custom_path):
        try:
            with open(custom_path, "r") as f:
                recipes = json.load(f)

            original_count = len(recipes)
            recipes = [r for r in recipes if r["id"] not in custom_ids_to_delete]
            deleted_count += original_count - len(recipes)

            with open(custom_path, "w") as f:
                json.dump(recipes, f, indent=2)

            print(f"✅ Deleted {original_count - len(recipes)} custom recipes from JSON")

        except Exception as e:
            print(f"❌ JSON delete error: {e}")

    return deleted_count


def delete_from_chromadb(recipe_ids: list, collection) -> bool:
    """Delete recipes from ChromaDB."""
    if collection is None:
        print("⚠️ ChromaDB not available, skipping")
        return False
    try:
        result = collection.get()
        if not result or not result['metadatas']:
            return False

        chroma_ids_to_delete = []
        for i, metadata in enumerate(result['metadatas']):
            recipe = json.loads(metadata['full_data'])
            if recipe['id'] in recipe_ids:
                chroma_ids_to_delete.append(result['ids'][i])  # ← make sure this line is indented with 4 spaces

        if chroma_ids_to_delete:
            collection.delete(ids=chroma_ids_to_delete)
            print(f"✅ Deleted {len(chroma_ids_to_delete)} from ChromaDB")
            return True

    except Exception as e:
        print(f"❌ ChromaDB delete error: {e}")
    return False

def delete_recipes(recipe_ids: list, collection) -> dict:
    """Main function — delete from data.py + JSON + ChromaDB."""
    json_count = delete_from_json(recipe_ids)
    chroma_ok = delete_from_chromadb(recipe_ids, collection)

    return {
        "json_deleted": json_count,
        "chroma_deleted": chroma_ok
    }