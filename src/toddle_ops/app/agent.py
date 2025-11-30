import asyncio
import os
import aiosqlite
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from typing import Any, Dict

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from toddle_ops.agents.root_agent.agent import root_agent
from toddle_ops.config.basic import events_compaction_config
from toddle_ops.services.sessions import session_service

# Load environment variables from .env
try:
    load_dotenv()
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
except Exception as e:
    print(f"Auth error: Details: {e}")

APP_NAME = "default"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

MODEL_NAME = "gemini-2.5-flash-lite"

adk_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    events_compaction_config=events_compaction_config,
)
