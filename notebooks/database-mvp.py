# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-adk==1.20.0",
#     "litellm==1.80.8",
#     "protobuf==6.33.2",
#     "pydantic==2.12.5",
#     "python-dotenv==1.2.1",
#     "sqlmodel==0.0.27",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.models.lite_llm import LiteLlm
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    return InMemoryRunner, LiteLlm, LlmAgent


@app.cell
def _():
    from enum import Enum
    from typing import List, Optional

    from pydantic import BaseModel

    from sqlmodel import SQLModel, Field, Relationship


    class ProjectBase(BaseModel):
        name: str = Field(index=True, description="The name of the project.")
        description: str = Field(description="A brief description of the project.")
        duration_minutes: int = Field(
            description="The estimated duration of the project in minutes."
        )
        instructions: str = Field(description="A list of instructions for the project.")


    class Project(ProjectBase, SQLModel, table=True):
        """A craft project for toddlers."""
        id: int | None = Field(default=None, primary_key=True)
        materials: list["Material"] = Relationship(back_populates="project")

    # materials_id: Optional[int] = Field(default=None, foreign_key="material.id")

    class MaterialBase(BaseModel):
        name: str = Field(index=True, description="The name of the material.")
        quantity: float = Field(description="The quantity of the material.")
        units: str | None = Field(default=None, description="The units of the material.")

    class Material(MaterialBase, SQLModel, table=True):
        """A material required for a project."""
        id: int | None = Field(default=None, primary_key=True)
        project_id: int | None = Field(default=None, foreign_key="project.id")
        project: Project | None = Relationship(back_populates="materials")

    class ProjectPackage(BaseModel):
        project: ProjectBase
        materials: List[MaterialBase]
    return (ProjectPackage,)


@app.cell
def _(LiteLlm, LlmAgent, ProjectPackage):
    project_conversion_agent = LlmAgent(
        name="project_conversion_agent",
        model=LiteLlm(model="ollama_chat/gemma3:4b"),
        instruction="""You are adept at converting the
        provided to you into Project and Material Classes.""",
        output_schema=ProjectPackage,
        output_key="project_dict",
    )
    return (project_conversion_agent,)


@app.cell
def _(InMemoryRunner, project_conversion_agent):
    runner = InMemoryRunner(agent=project_conversion_agent)
    return (runner,)


@app.cell
async def _(runner):
    await runner.run_debug()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
