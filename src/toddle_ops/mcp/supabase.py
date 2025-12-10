"""Supabase repository for handling CRUD operations for projects."""

from supabase import Client, create_client
from google.adk.tools import FunctionTool

from toddle_ops.config import supabase_settings
from toddle_ops.models.projects import StandardProject


class SupabaseRepo:
    """A repository for interacting with a Supabase 'projects' table."""

    def __init__(self, settings: dict | None = None):
        """
        Initializes the Supabase client.

        Args:
            settings: A dictionary with 'url' and 'key' for Supabase.
                      If not provided, it falls back to environment variables.
        """
        if settings and settings.get("url") and settings.get("key"):
            self.supabase_url = settings["url"]
            self.supabase_key = settings["key"]
        else:
            self.supabase_url = supabase_settings.url
            self.supabase_key = supabase_settings.key

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase URL and Key must be provided.")

        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def add_project(self, project: StandardProject) -> dict:
        """
        Adds a new project to the 'projects' table.

        Args:
            project: A StandardProject object to add.

        Returns:
            The newly created project data.
        """
        project_dict = project.model_dump()
        # The 'id' is auto-incrementing in the database, so we don't insert it.
        project_dict.pop("id", None)
        response = self.client.table("projects").insert(project_dict).execute()
        return response.data[0] if response.data else {}

    def get_project_by_name(self, name: str) -> dict | None:
        """
        Retrieves a project by its name.

        Args:
            name: The name of the project to retrieve.

        Returns:
            The project data or None if not found.
        """
        response = self.client.table("projects").select("*").eq("name", name).execute()
        return response.data[0] if response.data else None
    
    def get_project_by_id(self, project_id: int) -> dict | None:
        """
        Retrieves a project by its ID.

        Args:
            project_id: The ID of the project to retrieve.

        Returns:
            The project data or None if not found.
        """
        response = self.client.table("projects").select("*").eq("id", project_id).execute()
        return response.data[0] if response.data else None

    def list_projects(self) -> list[dict]:
        """
        Lists all projects in the 'projects' table.

        Returns:
            A list of all projects.
        """
        response = self.client.table("projects").select("*").execute()
        return response.data

    def update_project(self, project_id: int, updates: dict) -> dict:
        """
        Updates a project by its ID.

        Args:
            project_id: The ID of the project to update.
            updates: A dictionary of fields to update.

        Returns:
            The updated project data.
        """
        response = (
            self.client.table("projects")
            .update(updates)
            .eq("id", project_id)
            .execute()
        )
        return response.data[0] if response.data else {}

    def delete_project(self, project_id: int) -> dict:
        """
        Deletes a project by its ID.

        Args:
            project_id: The ID of the project to delete.
        
        Returns:
            The deleted project data.
        """
        response = self.client.table("projects").delete().eq("id", project_id).execute()
        return response.data[0] if response.data else {}


# Initialize a default repository instance for convenience
supabase_repo = SupabaseRepo()

# Create FunctionTools for agents to use
add_project_tool = FunctionTool(
    fn=supabase_repo.add_project,
    description="Adds a new toddler craft project to the Supabase database. Takes a StandardProject object.",
)

get_project_by_name_tool = FunctionTool(
    fn=supabase_repo.get_project_by_name,
    description="Retrieves a specific project from the database by its exact name.",
)

list_projects_tool = FunctionTool(
    fn=supabase_repo.list_projects,
    description="Lists all the toddler craft projects currently in the database.",
)

update_project_tool = FunctionTool(
    fn=supabase_repo.update_project,
    description="Updates an existing project in the database. Requires the project_id and a dictionary of updates.",
)

delete_project_tool = FunctionTool(
    fn=supabase_repo.delete_project,
    description="Deletes a project from the database by its project_id.",
)
