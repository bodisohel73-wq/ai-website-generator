import os
from typing import Optional


class Settings:
    """Production-ready application settings.

    All values are loaded from environment variables with secure and sensible defaults.
    """

    # MongoDB Configuration
    MONGO_URL: str = os.getenv(
        "MONGO_URL",
        "mongodb://localhost:27017"
    )
    DATABASE_NAME: str = os.getenv(
        "DATABASE_NAME",
        "html_generator"
    )

    # JWT Authentication
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET",
        "super-secret-jwt-key-change-this-in-production-please"
    )
    JWT_ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30"
        )
    )

    # Optional: Add more settings here in the future
    # Example:
    # DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


# Singleton settings instance (recommended import pattern)
settings = Settings()
