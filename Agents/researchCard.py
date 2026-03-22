import streamlit as st
from Agents.researchCrew import run_research_crew

def show_deep_research_button(recipe: dict, index: int = 0):
    """Renders a Deep Research button below each recipe."""
    
    recipe_key = f"{recipe['name'].replace(' ', '_').lower()}_{index}"
    state_key = f"researched_{recipe_key}"

    if st.button(
        "🔍 Deep Research this Recipe",
        key=f"research_{recipe_key}"
    ):
        with st.spinner("🤖 3 Agents researching, analysing nutrition and formatting... this may take a minute!"):
            result = run_research_crew(recipe['name'])
            if result:
                st.session_state[state_key] = result
            else:
                st.session_state[state_key] = {"error": "Research failed"}

    if state_key in st.session_state:
        result = st.session_state[state_key]

        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.success("✅ Deep Research Complete!")
            st.divider()

            st.markdown(f"### 🍽️ {result.get('name', 'N/A')}")

            col1, col2, col3 = st.columns(3)
            col1.metric("🌍 Cuisine", result.get("cuisine", "N/A"))
            col2.metric("📊 Difficulty", result.get("difficulty", "N/A"))
            col3.metric("🍴 Servings", result.get("servings", "N/A"))

            col4, col5 = st.columns(2)
            col4.metric("⏱️ Prep Time", result.get("prep_time", "N/A"))
            col5.metric("🔥 Cook Time", result.get("cooking_time", "N/A"))

            st.markdown("#### 🛒 Researched Ingredients")
            for ing in result.get("ingredients", []):
                st.markdown(f"- {ing}")

            st.markdown("#### 👨‍🍳 Instructions")
            st.markdown(result.get("instructions", "N/A"))

            st.markdown("#### 📊 Nutrition per Serving")
            col6, col7 = st.columns(2)
            col6.metric("🔥 Calories", f"{result.get('calories_per_serving', 'N/A')} kcal")
            col7.metric("⚠️ Dietary Info", result.get("dietary_info", "N/A"))

            if result.get("tips"):
                st.info(f"💡 **Tips:** {result['tips']}")