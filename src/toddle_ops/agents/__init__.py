"""
ToddleOps Agents Package

Provides agent factory and pre-configured agents for the ToddleOps system.
"""

from toddle_ops.agents.factory import (
    DEFAULT_MODEL,
    DEFAULT_SAFETY_SETTINGS,
    create_agent,
)

__all__ = [
    "create_agent",
    "DEFAULT_MODEL",
    "DEFAULT_SAFETY_SETTINGS",
]
