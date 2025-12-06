# database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

# Example:
# MONGODB_URL=mongodb+srv://USERNAME:PASSWORD@task-cluster.zl65poh.mongodb.net/taskdb?retryWrites=true&w=majority&appName=task-cluster
# DB_NAME=taskdb
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "taskdb")

# Print configuration on startup (without showing password)
if MONGODB_URL and "mongodb+srv://" in MONGODB_URL:
    # Hide password in URL for security
    safe_url = MONGODB_URL.split("@")[0].split("://")[0] + "://***@" + MONGODB_URL.split("@")[1] if "@" in MONGODB_URL else MONGODB_URL
    print(f"📝 Using MongoDB Atlas: {safe_url}")
    print(f"📝 Database name: {DB_NAME}")
else:
    print(f"📝 Using local MongoDB: {MONGODB_URL}")
    print(f"📝 Database name: {DB_NAME}")

client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    """
    Create a global MongoDB client and DB instance.
    Called once on FastAPI startup.
    """
    global client, _db

    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        _db = client[DB_NAME]
        
        # Test the connection
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise


async def close_mongo_connection() -> None:
    """
    Close MongoDB connection on app shutdown.
    """
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """
    Dependency / helper to get the current DB.
    """
    if _db is None:
        raise RuntimeError("Database not initialized. Did you call connect_to_mongo() on startup?")
    return _db
