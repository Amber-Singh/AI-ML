import os
import warnings

# --- 1. SAFETY FIRST (Must be before other imports) ---
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

try:
    import posthog
    posthog.capture = lambda *args, **kwargs: None
except ImportError:
    pass

warnings.filterwarnings("ignore")

# --- 2. NOW IMPORT EVERYTHING ELSE ---
from dotenv import load_dotenv
import streamlit as st
import json 
import uuid
from groq import Groq
from utils import verify_login  # Now this will use the safety settings
from Agents.agents import create_recipe_agent
from Agents.tasks import create_recipe_task
from crewai import Crew, Process
from pdfFeature import create_pdf_download_button  
from nutritionCard import show_nutrition_card
from translateCard import show_translate_button
from Data.recepies import search_recipes, get_collection
from addRecipeCard import show_add_recipe_form
from addRecipeFeature import save_recipe_to_chromadb, save_recipe_to_data_py
from Agents.researchCard import show_deep_research_button
from recipeManager import show_recipe_manager

load_dotenv()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
def generate_recipe(query):
    """Generate recipe using Groq API"""
    try:
        
        recipe_agent = create_recipe_agent()
        recipe_task = create_recipe_task(recipe_agent,query)
        recipe_crew = Crew(
            agents=[recipe_agent],
            tasks=[recipe_task],
            process=Process.sequential,
            memory=False,      # <--- MUST BE FALSE
            verbose=True
        )
        result = recipe_crew.kickoff()
        
        raw = result.raw if hasattr(result, 'raw') else str(result)
        raw = raw.encode('utf-8', errors='ignore').decode('utf-8')
        raw = raw.strip()
        # Parse result into your data format
        raw = str(result).strip()
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        
        recipe = json.loads(raw)
        recipe["id"] = str(uuid.uuid4())
        return recipe 
    except Exception as e:
        return f"Error: {str(e)[:150]}"

def login_page():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if verify_login(username, password):  # ← Uses verify_login!
            st.session_state.logged_in = True
            st.rerun()
            
def main():
    st.title("🍽️ Recipe AI Chat")
        
    tab1, tab2 = st.tabs(["💬 Chat", "📋 Recipe Manager"])
    
    with tab1:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "current_recipes" not in st.session_state:
            st.session_state.current_recipes = []
        
        # 1. Chat history first
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 2. Feature buttons AFTER chat history (appears below messages)
        if st.session_state.current_recipes:
            for i,recipe in enumerate(st.session_state.current_recipes):
                st.divider()
                create_pdf_download_button(recipe, button_label="📄 Download Search Results as PDF")
                show_nutrition_card(recipe)
                show_translate_button(recipe,index =i)
                show_deep_research_button(recipe,index =i)
        
        # Add recipe form — always visible below
        st.divider()
        show_add_recipe_form(get_collection()) 

        # 3. Chat input at bottom
        if prompt := st.chat_input("Search for a recipe..."):
            st.session_state.current_recipes = []  # clear old results
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
                
            results = search_recipes(prompt)
            if results:
                st.session_state.current_recipes = results
                response = f"Found {len(results)} recipe(s):\n\n"
                for recipe in results:
                    response += f"**{recipe['name']}**\nIngredients: {', '.join(recipe['ingredients'][:3])}...\n\n"
            else:
                results = generate_recipe(prompt)
                save_recipe_to_chromadb(results, get_collection())
                save_recipe_to_data_py(results)
                if isinstance(results, dict):
                    st.session_state.current_recipes = [results]
                    response = f"Generated **{results['name']}** recipe!\n\n"
                    response += f"**Cuisine:** {results['cuisine']}\n"
                    response += f"**Difficulty:** {results['difficulty']}\n"
                    response += f"**Cooking Time:** {results['cooking_time']}\n"
                    response += f"**Ingredients:** {', '.join(results['ingredients'][:3])}...\n"
                else:
                    response = str(results)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            
            st.rerun()  # ← KEY FIX: rerun so buttons render AFTER messages
    with tab2:
        show_recipe_manager()


if __name__ == "__main__":
    if st.session_state.logged_in:
        main()  # Your chat app
    else:
        login_page()