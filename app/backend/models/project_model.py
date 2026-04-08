from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    """Production-ready Pydantic model for MongoDB Project collection.

    Used for:
    - API request/response validation
    - Internal service layer
    - MongoDB document mapping via helper
    """

    id: Optional[str] = Field(
        None,
        description="Project ID (MongoDB _id converted to string)",
        alias="_id",
    )
    user_id: str = Field(..., description="ID of the user who owns this project")
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Project description")
    html_content: str = Field(..., description="Generated HTML content")
    created_at: datetime = Field(..., description="Project creation timestamp")


def project_helper(project: dict) -> dict:
    """Convert raw MongoDB document (with ObjectId) to clean dictionary.

    This is the standard helper used across the application to:
    - Convert ObjectId to str for JSON serialization
    - Map MongoDB '_id' field to Pydantic 'id' field
    - Ensure consistent data shape for services and API responses

    Usage:
        project_doc = collection.find_one(...)
        project_dict = project_helper(project_doc)
        project = Project(**project_dict)
    """
    if not project:
        return {}

    return {
        "id": str(project["_id"]) if "_id" in project and project["_id"] else None,
        "user_id": project.get("user_id"),
        "title": project.get("title"),
        "description": project.get("description"),
        "html_content": project.get("html_content"),
        "created_at": project.get("created_at"),
    }
