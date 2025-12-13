import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner

from toddle_ops.app import app
from toddle_ops.services.memory import memory_service
from toddle_ops.services.sessions import session_service

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object
runner = Runner(app=app, session_service=session_service, memory_service=memory_service)


async def main():
    try:  
        response = await runner.run_debug("Hello there! I would like a project please.")

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
