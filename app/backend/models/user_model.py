from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """Production-ready Pydantic model for MongoDB User collection.

    Used for:
    - API request/response validation
    - Internal service layer
    - MongoDB document mapping via helper
    """

    id: Optional[str] = Field(
        None,
        description="User ID (MongoDB _id converted to string)",
        alias="_id",
    )
    email: str = Field(..., description="Unique user email address")
    password: str = Field(..., description="Hashed password (never returned in public responses)")
    created_at: datetime = Field(..., description="Account creation timestamp")


def user_helper(user: dict) -> dict:
    """Convert raw MongoDB document (with ObjectId) to clean dictionary.

    This is the standard helper used across the application to:
    - Convert ObjectId to str for JSON serialization
    - Map MongoDB '_id' field to Pydantic 'id' field
    - Ensure consistent data shape for services and API responses

    Usage:
        user_doc = collection.find_one(...)
        user_dict = user_helper(user_doc)
        user = User(**user_dict)
    """
    if not user:
        return {}

    return {
        "id": str(user["_id"]) if "_id" in user and user["_id"] else None,
        "email": user.get("email"),
        "password": user.get("password"),
        "created_at": user.get("created_at"),
    }
