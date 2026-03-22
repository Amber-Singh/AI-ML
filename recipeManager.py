import streamlit as st
from deleteRecipe import delete_recipes
from Data.recepies import get_recipes, get_collection
import json
import os
import pandas as pd

def show_recipe_manager():
    """Show all recipes in a table with checkboxes and delete option."""
    
    st.markdown("## 📋 Recipe Manager")
    st.caption("Select recipes to delete using the checkboxes in the table.")

    # Fetch all recipes
    recipes = get_recipes()
    
    if not recipes:
        st.info("No recipes found!")
        return

    # Load custom recipe IDs
    custom_ids = set()
    if os.path.exists("Data/custom_recipes.json"):
        try:
            with open("Data/custom_recipes.json", "r") as f:
                custom = json.load(f)
                custom_ids = {r["id"] for r in custom}
        except:
            pass

    st.markdown(f"**Total Recipes: {len(recipes)}**")
    st.divider()

    # Build dataframe
    data = []
    for recipe in recipes:
        data.append({
            "Select": False,
            "Name": recipe["name"],
            "Cuisine": recipe.get("cuisine", "N/A"),
            "Difficulty": recipe.get("difficulty", "N/A"),
            "Cooking Time": recipe.get("cooking_time", "N/A"),
            "Servings": recipe.get("servings", "N/A"),
            "Type": "🟢 Custom" if recipe["id"] in custom_ids else "🔵 Sample",
            "_id": recipe["id"]  # hidden reference
        })

    df = pd.DataFrame(data)

    # Editable table with checkboxes
    edited_df = st.data_editor(
        df.drop(columns=["_id"]),  # hide _id from display
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(
                "Select",
                help="Check to select for deletion",
                default=False
            )
        },
        key="recipe_table"
    )

    st.divider()

    # Get selected recipe IDs
    selected_indices = edited_df[edited_df["Select"] == True].index.tolist()
    selected_ids = [data[i]["_id"] for i in selected_indices]
    selected_names = [data[i]["Name"] for i in selected_indices]
    selected_count = len(selected_ids)

    if selected_count > 0:
        st.warning(f"⚠️ **{selected_count} recipe(s) selected:** {', '.join(selected_names)}")

        confirm = st.checkbox(
            "✅ I confirm I want to delete selected recipes",
            key="delete_confirm"
        )

        if st.button(
            f"🗑️ Delete {selected_count} Recipe(s)",
            type="primary",
            disabled=not confirm,
            key="delete_btn"
        ):
            with st.spinner("Deleting recipes..."):
                collection = get_collection()
                result = delete_recipes(selected_ids, collection)

            if result["json_deleted"] > 0:
                st.success(f"✅ Deleted {result['json_deleted']} custom recipe(s) permanently!")
            if result["chroma_deleted"]:
                st.success("✅ Removed from search database!")
            
            st.session_state.current_recipes = []
            st.rerun()
    else:
        st.info("☝️ Check the boxes in the table above to select recipes for deletion")