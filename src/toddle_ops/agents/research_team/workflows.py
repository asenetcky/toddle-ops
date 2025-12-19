from google.adk.agents import ParallelAgent, SequentialAgent

from toddle_ops.agents.research_team.sub_agent import (
    get_high_temp_project_researcher,
    get_low_temp_project_researcher,
    get_project_synthesizer,
)


def get_research_parallel() -> ParallelAgent:
    """Creates a ParallelAgent that runs high and low temperature project researchers."""
    return ParallelAgent(
        name="ResearchParallel",
        sub_agents=[
            get_high_temp_project_researcher(),
            get_low_temp_project_researcher(),
        ],
    )


def get_research_sequence() -> SequentialAgent:
    """Creates a SequentialAgent that first runs research in parallel, then synthesizes the project."""
    research_parallel = get_research_parallel()
    return SequentialAgent(
        name="ResearchSequence",
        sub_agents=[research_parallel, get_project_synthesizer()],
    )
