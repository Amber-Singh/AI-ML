import streamlit as st
from translateFeature import translate_recipe

SUPPORTED_LANGUAGES = {
    "🇮🇳 Hindi": "Hindi",
    "🇪🇸 Spanish": "Spanish",
}

def show_translate_button(recipe: dict, index: int = 0):
    """Renders a translate button with language selector below each recipe."""

    recipe_key = f"{recipe['name'].replace(' ', '_').lower()}_{index}"
    state_key = f"translated_{recipe_key}"

    st.markdown("#### 🌐 Translate Recipe")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_label = st.selectbox(
            "Select language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            key=f"lang_{recipe_key}"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        translate_clicked = st.button("Translate 🌐", key=f"translate_{recipe_key}")

    # Store translation result in session_state
    if translate_clicked:
        st.write("Button clicked!")  # ← ADD THIS
        target_language = SUPPORTED_LANGUAGES[selected_label]
        with st.spinner(f"Translating to {target_language}..."):
            try:
                translated = translate_recipe(recipe, target_language)
                # Save result + language to session state
                st.session_state[state_key] = {
                    "data": translated,
                    "language": target_language
                }
            except Exception as e:
                st.session_state[state_key] = {"error": str(e)}

    # Render from session_state (persists across reruns)
    if state_key in st.session_state:
        result = st.session_state[state_key]

        if "error" in result:
            st.error(f"❌ Translation failed: {result['error']}")
        else:
            translated = result["data"]
            language = result["language"]

            st.success(f"✅ Translated to {language}!")
            st.divider()

            # Recipe Name
            st.markdown(f"### 🍽️ {translated.get('name', 'N/A')}")

            # Ingredients
            st.markdown("#### 🛒 Ingredients")
            for ingredient in translated.get("ingredients", []):
                st.markdown(f"- {ingredient}")

            # Instructions
            st.markdown("#### 👨‍🍳 Instructions")
            st.markdown(translated.get("instructions", "N/A"))

            # Tips
            if translated.get("tips"):
                st.markdown("#### 💡 Tips")
                st.info(translated.get("tips"))