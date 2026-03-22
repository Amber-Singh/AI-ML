from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from crewai import Agent, LLM
# Load environment variables from .env file
load_dotenv()

# Initialize the LLM (Groq)


groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_recipe_agent():
    """
    Define the Recipe Creator Agent
    
    This agent is a professional chef who creates detailed recipes
    """

    
    # Create and return the agent
    agent = Agent(
        role="Professional Recipe Creator",
        
        goal="Create delicious, detailed, and easy-to-follow recipes based on "
             "user requirements. Make recipes that anyone can cook at home.",
        
        backstory="You are a professional chef with 20 years of experience in "
                 "international cuisine. You specialize in creating recipes that "
                 "are both delicious and practical for home cooks. You understand "
                 "flavor profiles, cooking techniques, and how to write clear "
                 "instructions that beginners can follow.",
        
        llm=groq_llm,
        verbose=True,
        memory=False,         # Already set
        cache=False,          # <--- DISABLE this (prevents SQLite/Chroma writes)
        embedder=None,        # <--- FORCE this to None (prevents ONNX loading)
        allow_delegation=False, # Optional: keeps logic simple
    )
    
    return agent