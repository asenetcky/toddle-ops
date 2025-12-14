import os

from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService

load_dotenv()

SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
SUPABASE_USER = os.getenv("SUPABASE_USER")

# basic session service using Supabase Postgres
db_url = f"postgresql+asyncpg://{SUPABASE_USER}:{SUPABASE_PASSWORD}@aws-0-us-west-2.pooler.supabase.com:5432/postgres"
session_service = DatabaseSessionService(db_url=db_url)
