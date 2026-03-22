import streamlit as st
from addRecipeFeature import save_recipe_to_chromadb, save_recipe_to_data_py
import uuid

def show_add_recipe_form(collection):
    """Show a Streamlit form to collect recipe details."""

    with st.expander("➕ Add New Recipe", expanded=False):
        with st.form("add_recipe_form"):
            st.markdown("### 📝 Add Your Recipe")

            # Row 1
            col1, col2 = st.columns(2)
            name = col1.text_input("🍽️ Recipe Name *", placeholder="e.g. Butter Chicken")
            cuisine = col2.text_input("🌍 Cuisine *", placeholder="e.g. Indian")

            # Row 2
            col3, col4 = st.columns(2)
            cooking_time = col3.text_input("🔥 Cooking Time *", placeholder="e.g. 35 minutes")
            prep_time = col4.text_input("⏱️ Prep Time *", placeholder="e.g. 20 minutes")

            # Row 3
            col5, col6, col7 = st.columns(3)
            difficulty = col5.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])
            servings = col6.text_input("🍴 Servings", placeholder="e.g. 4")
            calories = col7.text_input("🔥 Calories/Serving", placeholder="e.g. 420")

            # Ingredients
            ingredients_raw = st.text_area(
                "🛒 Ingredients * (one per line)",
                placeholder="500g chicken breast\n200g yogurt\n2 tbsp tikka paste",
                height=150
            )

            # Instructions
            instructions = st.text_area(
                "👨‍🍳 Instructions *",
                placeholder="1. Marinate chicken...\n2. Heat pan...\n3. Cook sauce...",
                height=200
            )

            # Row 4
            dietary_info = st.text_input(
                "⚠️ Dietary Info",
                placeholder="e.g. Contains dairy, Gluten-free"
            )
            tips = st.text_input(
                "💡 Tips",
                placeholder="e.g. Marinate longer for deeper flavor"
            )

            submitted = st.form_submit_button("💾 Save Recipe")

            if submitted:
                # Validate required fields
                if not name or not cuisine or not ingredients_raw or not instructions:
                    st.error("❌ Please fill in all required fields marked with *")
                    return

                # Build recipe dict
                ingredients_list = [
                    ing.strip()
                    for ing in ingredients_raw.strip().split("\n")
                    if ing.strip()
                ]

                recipe = {
                    "id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "cuisine": cuisine.strip(),
                    "ingredients": ingredients_list,
                    "instructions": instructions.strip(),
                    "cooking_time": cooking_time.strip() or "Unknown",
                    "prep_time": prep_time.strip() or "Unknown",
                    "difficulty": difficulty,
                    "servings": servings.strip() or "Unknown",
                    "calories_per_serving": calories.strip() or "Unknown",
                    "dietary_info": dietary_info.strip() or "Unknown",
                    "tips": tips.strip() or ""
                }

                # Save to ChromaDB + data.py
                with st.spinner("Saving recipe..."):
                    chroma_ok = save_recipe_to_chromadb(recipe, collection)
                    file_ok = save_recipe_to_data_py(recipe)

                if chroma_ok and file_ok:
                    st.success(f"✅ **{recipe['name']}** saved successfully!")

                    # Show summary
                    st.markdown("#### 📋 Saved Recipe Summary")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("🌍 Cuisine", recipe["cuisine"])
                    c2.metric("📊 Difficulty", recipe["difficulty"])
                    c3.metric("🍴 Servings", recipe["servings"])

                    st.markdown("**🛒 Ingredients:**")
                    for ing in recipe["ingredients"]:
                        st.markdown(f"- {ing}")
                else:
                    st.error("❌ Something went wrong while saving. Please try again.")