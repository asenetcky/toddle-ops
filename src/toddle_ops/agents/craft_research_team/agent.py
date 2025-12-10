from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from toddle_ops.config import retry_config
from toddle_ops.models.projects import StandardProject

project_researcher = LlmAgent(
    name="ProjectResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Using google_search, research safe crafts and projects for toddlers 
    that are easy to do at home with common household materials. 

    - You WILL ONLY provide one project. 
    - Be sure to include at least the following:
        - the project name 
        - duration of project
        - required materials for project
        - step by step instructions
    """,
    tools=[google_search],
    output_key="project_research",
)

project_synthesizer = LlmAgent(
    name="ProjectSynthesizer",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a project synthesizer. You will receive research 
    for toddler projects from the ProjectResearcher. 
    
    Your task is to analyze the research output and create a single, 
    sensible project. You can either pick the best parts from the project from 
    the provided research, or combine elements to create a new project.

    Research Outputs: {project_research}

    Your output MUST be a `StandardProject` object.
    """,
    output_schema=StandardProject,
    output_key="standard_project",
)

# TODO implement a loop possible a human in the loop for feedback etc...

# Your output MUST be a single `Project` object.
# prolly should separate the project schema out from this.
# one should be user facing, the other for future database manipulations

root_agent = SequentialAgent(
    name="CraftResearchPipeline",
    sub_agents=[project_researcher, project_synthesizer],
)
