"""
Main entry point for the ToddleOps application.
This file is used when running the app via `adk web` or deploying with Docker.
"""
import os
from pathlib import Path

# Ensure we're in the correct directory
if __name__ == "__main__":
    # The app is defined in src/toddle_ops/agents/root_agent/agent.py
    # and can be run with: adk web --app-path src/toddle_ops/agents/root_agent/agent.py
    print("ToddleOps Application")
    print("=====================")
    print("To run the application, use:")
    print("  adk web src/toddle_ops/agents")
    print("")
    print("Or use the Makefile:")
    print("  make run")
