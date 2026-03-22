import streamlit as st
from nutritionFeature import get_nutrition_from_groq

def show_nutrition_card(recipe: dict):
    """Renders an expander button with a Groq AI nutrition summary card."""
    
    with st.expander("🥗 View Nutrition Info (AI Estimated)"):
        with st.spinner("Analysing nutrition with Groq AI..."):
            try:
                nutrition = get_nutrition_from_groq(
                    recipe_name=recipe["name"],
                    ingredients=recipe["ingredients"]
                )
                
                st.markdown(f"### 📊 Nutrition per serving — *{recipe['name']}*")
                st.caption("⚠️ AI-estimated values. Not a substitute for professional dietary advice.")
                
                st.divider()
                
                # Row 1 — Main macros
                col1, col2, col3 = st.columns(3)
                col1.metric("🔥 Calories", f"{nutrition.get('calories', 'N/A')} kcal")
                col2.metric("🥩 Protein",  f"{nutrition.get('protein_g', 'N/A')} g")
                col3.metric("🍞 Carbs",    f"{nutrition.get('carbs_g', 'N/A')} g")
                
                st.divider()
                
                # Row 2 — Secondary macros
                col4, col5, col6 = st.columns(3)
                col4.metric("🧈 Fat",   f"{nutrition.get('fat_g', 'N/A')} g")
                col5.metric("🌾 Fiber", f"{nutrition.get('fiber_g', 'N/A')} g")
                col6.metric("🍬 Sugar", f"{nutrition.get('sugar_g', 'N/A')} g")
                
                st.divider()
                
                # Row 3 — Sodium
                st.metric("🧂 Sodium", f"{nutrition.get('sodium_mg', 'N/A')} mg")
                
                st.success("✅ Nutrition analysis complete!")

            except Exception as e:
                st.error(f"❌ Could not estimate nutrition: {str(e)}")