from google.adk.agents import LoopAgent, SequentialAgent

from toddle_ops.agents.quality_assurance_team.sub_agent import (
    get_editorial_agent,
    get_safety_critic_agent,
    get_safety_refiner_agent,
)

# Workflows for Quality Assurance Team Agents


def get_safety_refinement_loop() -> LoopAgent:
    """Creates the Safety Refinement Loop as a Loop Agent."""
    return LoopAgent(
        name="SafetyRefinementLoop",
        sub_agents=[get_safety_critic_agent(), get_safety_refiner_agent()],
        max_iterations=1,
    )


# Define the Safety Refinement Loop as a Loop Agent
def get_quality_assurance_sequence() -> SequentialAgent:
    """Creates the Quality Assurance Sequence."""
    safety_refinement_loop = get_safety_refinement_loop()
    return SequentialAgent(
        name="QualityAssuranceSequence",
        sub_agents=[safety_refinement_loop, get_editorial_agent()],
    )
