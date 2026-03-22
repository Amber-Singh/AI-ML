from crewai import Agent
from langchain_groq import ChatGroq
import os

def create_research_crew_agents():
    llm = ChatGroq(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Agent 1 — Recipe Researcher
    researcher = Agent(
        role="Recipe Researcher",
        goal="Research and gather complete, authentic recipe details",
        backstory="""You are an expert culinary researcher with deep knowledge 
        of world cuisines. You find accurate, detailed recipes with proper 
        ingredients and cooking techniques.""",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        memory=False
    )

    # Agent 2 — Nutrition Analyst
    nutritionist = Agent(
        role="Nutrition Analyst",
        goal="Analyse recipe ingredients and provide accurate nutrition information",
        backstory="""You are a certified nutritionist who specializes in 
        analysing food recipes. You estimate macronutrients accurately and 
        identify dietary information like gluten-free, vegan, contains dairy etc.""",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        memory=False
    )

    # Agent 3 — Recipe Formatter
    formatter = Agent(
        role="Recipe Formatter",
        goal="Format recipe and nutrition data into a clean structured JSON format",
        backstory="""You are a data formatting expert who takes raw recipe 
        and nutrition information and structures it perfectly into JSON format. 
        You ensure all fields are present and correctly formatted.""",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        memory=False
    )

    return researcher, nutritionist, formatter