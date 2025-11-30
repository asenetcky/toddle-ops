import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent

import toddle_ops.agents.root_agent.agent as root
from toddle_ops.config.basic import events_compaction_config
from google.adk.plugins.logging_plugin import LoggingPlugin
import vertexai

# Load environment variables from .env
try:
    load_dotenv()
    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"],
    )
except Exception as e:
    print(f"Auth error: Details: {e}")

root_agent = root.root_agent
