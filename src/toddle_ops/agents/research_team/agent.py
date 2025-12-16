from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from toddle_ops.config import retry_config
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.models.projects import StandardProject
from toddle_ops.agents.research_team.sub_agent import default_temp_project_researcher
from toddle_ops.agents.research_team.workflows import research_sequence
from google.adk.tools import AgentTool


# Define instructions for the Project Synthesizer Agent
research_coordinator_instructions = AgentInstructions(
    persona="Project Research Coordinator",
    primary_objective=[
        "Coordinate the research team to create a safe and engaging toddler project suitable for children aged 1-3 years."
    ],
    rules=[
        "You MUST use your tools to delegate tasks.",
        "Use the research_sequence to gather diverse project ideas.",
        "Use the default_temp_project_researcher to explore specific project ideas when coordinating with the Orchestrator Agent."
    ],
    constraints=[],
    incoming_keys=["StandardProject"],
)

# Create the Project Synthesizer Agent using the defined instructions


root_agent = LlmAgent(
    name="ProjectResearchCoordinator",
    description="Coordinates research team to create toddler projects.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=research_coordinator_instructions.format_instructions(),
    output_schema=StandardProject,
    output_key="standard_project",
    tools=[
       AgentTool(research_sequence),
       AgentTool(default_temp_project_researcher), 
    ],
)