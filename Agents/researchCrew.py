import os
import json
import uuid
from crewai import Crew, Process
from Agents.researchAgents import create_research_crew_agents
from Agents.reasearchTasks import create_research_tasks

def run_research_crew(query: str) -> dict:
    """Run 3-agent research crew and return structured recipe."""
    try:
        # Create agents
        researcher, nutritionist, formatter = create_research_crew_agents()
        
        # Create tasks
        tasks = create_research_tasks(researcher, nutritionist, formatter, query)
        
        # Create crew
        crew = Crew(
            agents=[researcher, nutritionist, formatter],
            tasks=tasks,
            process=Process.sequential,
            memory=False,
            verbose=True
        )
        
        # Run crew
        result = crew.kickoff()
        
        # Parse final JSON output
        raw = result.raw if hasattr(result, 'raw') else str(result)
        raw = raw.encode('utf-8', errors='ignore').decode('utf-8').strip()
        
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        
        recipe = json.loads(raw)
        recipe["id"] = str(uuid.uuid4())
        return recipe

    except Exception as e:
        print(f"Research crew error: {e}")
        return None