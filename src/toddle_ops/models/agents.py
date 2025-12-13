from typing import Annotated
from pydantic import BaseModel, Field

class AgentInstructions(BaseModel):
    """
    A model representing the instructions for an AI agent.
    
    Attributes:
        persona (str): The persona of the agent.
        primary_objective (list[str]): The primary objectives of the agent.
        rules (list[str]): The rules the agent must follow.
        constraints (list[str]): The constraints the agent must follow.
        incoming_keys (list[str]): The incoming keys the agent will receive.    
    """
    persona: Annotated[str, Field(default="helpful assistant", description="The persona of the agent.")]   
    primary_objective: Annotated[list[str], Field(description="The primary objectives of the agent.")]
    rules: Annotated[list[str] | None, Field(default_factory=list, description="The rules the agent must follow.")]
    constraints: Annotated[list[str] | None, Field(default_factory=list, description="The constraints the agent must follow.")]
    incoming_keys: Annotated[list[str] | None, Field(default_factory=list, description="The incoming keys the agent will receive.")]

    def format_instructions(self) -> str:
        """
        Format the agent instructions into a structured string.

        Returns:
            str: The formatted instructions.
        """

        objectives = "".join(f"\t- {obj}\n" for obj in self.primary_objective)    
        rules = "".join(f"\t- {rule}\n" for rule in self.rules)
        constraints = "".join(f"\t- {constraint}\n" for constraint in self.constraints)
        incoming_keys = "".join(f"\t- {{{key}}}\n" for key in self.incoming_keys)
        
        instructions = (
            f"Persona: You are a {self.persona}\n\n"
            f"Your primary objectives are:\n"
            f"{objectives}\n"
            f"Please adhere to the following rules:\n"
            f"{rules}\n"
            f"You must NEVER do the following:\n"
            f"{constraints}\n"
            f"You will receive the following incoming keys:\n"
            f"{incoming_keys}"
        )

        return instructions
