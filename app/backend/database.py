from pymongo import MongoClient
from pymongo.database import Database

from config import settings


# Production-ready MongoDB client with connection pooling
# Created once at module import time (standard and efficient pattern)
client: MongoClient = MongoClient(
    settings.MONGO_URL,
    # Best practices for production
    maxPoolSize=100,
    minPoolSize=10,
    maxIdleTimeMS=90000,
    connectTimeoutMS=30000,
    socketTimeoutMS=60000,
)

# Database instance
db: Database = client[settings.DATABASE_NAME]


def get_db() -> Database:
    """Return the MongoDB database instance.
    
    Recommended usage:
    - In FastAPI routes: db = Depends(get_db)
    - Or import directly in services/repositories.
    
    This function ensures the same database instance is reused across the application.
    """
    return db


# Optional: Graceful shutdown helper (call in FastAPI lifespan or on shutdown)
def close_db_connection() -> None:
    """Close MongoDB client connection (for clean shutdown)."""
    global client
    if client is not None:
        client.close()
