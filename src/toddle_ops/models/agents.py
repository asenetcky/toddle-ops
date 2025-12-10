from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Kinds of agents the system knows about."""

    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"


class OrchestrationStyle(str, Enum):
    """How an orchestrator coordinates the agents it manages."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class AgentToolSpec(BaseModel):
    """Metadata describing another agent exposed as a google-adk AgentTool."""

    handle: str = Field(
        ..., description="Name used when exposing the managed agent as an AgentTool."
    )
    agent_path: str = Field(
        ..., description="Dotted import path to the underlying agent instance."
    )
    summary: str | None = Field(
        None, description="Short reminder of when or why to call this agent."
    )
    input_keys: List[str] = Field(
        default_factory=list,
        description="Context keys the managed agent expects as input.",
    )
    output_keys: List[str] = Field(
        default_factory=list,
        description="Keys made available after the managed agent finishes.",
    )


class AgentArchetype(BaseModel):
    """Base data for describing an agent before wiring it up."""

    name: str
    summary: str
    instruction: str
    model: str = Field(
        ..., description="Model identifier (e.g., gemini-2.5-flash-lite, ollama_chat/mistral-nemo:12b)."
    )
    type: AgentType = Field(
        ..., description="What category of agent this archetype represents."
    )
    default_tools: List[str] = Field(
        default_factory=list, description="Non-agent tools to attach by default."
    )
    output_key: str | None = Field(
        None, description="Primary output key the agent should populate, if any."
    )


class OrchestratorAgentArchetype(AgentArchetype):
    """Agent that coordinates other agents exposed as AgentTools."""

    type: AgentType = Field(
        default=AgentType.ORCHESTRATOR,
        const=True,
        description="Locked to orchestrator archetype.",
    )
    orchestration_style: OrchestrationStyle = Field(
        default=OrchestrationStyle.SEQUENTIAL,
        description="Preferred coordination style for managed agents.",
    )
    managed_agents: List[AgentToolSpec] = Field(
        default_factory=list,
        description="Agents this orchestrator can invoke via AgentTool wrappers.",
    )


class WorkerAgentArchetype(AgentArchetype):
    """Single-purpose worker agent with optional helper tools."""

    type: AgentType = Field(
        default=AgentType.WORKER,
        const=True,
        description="Locked to worker archetype.",
    )
    capability: str = Field(
        ..., description="What the worker is primarily responsible for doing."
    )
    accepted_inputs: List[str] = Field(
        default_factory=list,
        description="Input keys this worker expects (e.g., standard_project, user_prompt).",
    )
    produces: List[str] = Field(
        default_factory=list,
        description="Output keys this worker emits when it finishes.",
    )
    helper_tools: List[str] = Field(
        default_factory=list,
        description="Non-agent tools that should be registered for this worker (e.g., search).",
    )
