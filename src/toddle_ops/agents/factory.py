"""
Agent Factory Module

Provides a centralized factory function for creating LlmAgent instances
with sensible defaults, reducing boilerplate across the codebase.
"""

from typing import Any, Callable

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from toddle_ops.config import retry_config

# Default model configuration
DEFAULT_MODEL = "gemini-2.5-flash-lite"

# Default safety settings for toddler-focused content
DEFAULT_SAFETY_SETTINGS = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    )
]


def create_agent(
    name: str,
    description: str,
    instruction: str,
    *,
    output_key: str | None = None,
    output_schema: type | None = None,
    model: str = DEFAULT_MODEL,
    tools: list[Any] | None = None,
    sub_agents: list[Any] | None = None,
    temperature: float | None = None,
    max_output_tokens: int | None = None,
    safety_settings: list[types.SafetySetting] | None = None,
    before_agent_callback: Callable[..., Any] | None = None,
    after_agent_callback: Callable[..., Any] | None = None,
    generate_content_config: types.GenerateContentConfig | None = None,
) -> LlmAgent:
    """
    Factory function to create an LlmAgent with sensible defaults.

    This function centralizes agent creation logic, ensuring consistent
    configuration across all agents in the application.

    Args:
        name: The agent's name (used for identification and logging).
        description: A brief description of the agent's purpose.
        instruction: The system instruction/prompt for the agent.
        output_key: Key to store the agent's output in session state.
        output_schema: Pydantic model for structured output.
        model: The Gemini model to use (defaults to gemini-2.5-flash-lite).
        tools: List of tools available to the agent.
        sub_agents: List of sub-agents this agent can delegate to.
        temperature: Sampling temperature for generation.
        max_output_tokens: Maximum tokens in the response.
        safety_settings: Custom safety settings (defaults to child-safe settings).
        before_agent_callback: Callback executed before agent runs.
        after_agent_callback: Callback executed after agent runs.
        generate_content_config: Full config object (overrides temperature/max_tokens/safety).

    Returns:
        A configured LlmAgent instance.

    Example:
        >>> agent = create_agent(
        ...     name="MyAgent",
        ...     description="Does something useful",
        ...     instruction="You are a helpful assistant.",
        ...     output_key="result",
        ...     temperature=0.7,
        ... )
    """
    # Build generate_content_config if individual params are provided
    # but no full config was passed
    if generate_content_config is None and any(
        [
            temperature is not None,
            max_output_tokens is not None,
            safety_settings is not None,
        ]
    ):
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            safety_settings=safety_settings or DEFAULT_SAFETY_SETTINGS,
        )

    # Build kwargs dict, only including non-None values
    kwargs: dict[str, Any] = {
        "name": name,
        "description": description,
        "model": Gemini(model=model, retry_options=retry_config),
        "instruction": instruction,
    }

    # Add optional parameters only if they have values
    if output_key is not None:
        kwargs["output_key"] = output_key
    if output_schema is not None:
        kwargs["output_schema"] = output_schema
    if tools:
        kwargs["tools"] = tools
    if sub_agents:
        kwargs["sub_agents"] = sub_agents
    if generate_content_config is not None:
        kwargs["generate_content_config"] = generate_content_config
    if before_agent_callback is not None:
        kwargs["before_agent_callback"] = before_agent_callback
    if after_agent_callback is not None:
        kwargs["after_agent_callback"] = after_agent_callback

    return LlmAgent(**kwargs)
