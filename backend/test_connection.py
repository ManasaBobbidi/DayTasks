"""
Quick test script to verify database connection and data access.
Run this to check if everything is working before starting the server.
"""
import asyncio
import sys
from database import connect_to_mongo, get_database, close_mongo_connection
from models import Task


async def test_connection():
    """Test MongoDB connection and basic CRUD operations."""
    try:
        print("🔍 Testing MongoDB connection...")
        await connect_to_mongo()
        
        db = get_database()
        print("✅ Database connection successful!")
        
        # Test: Create a test task
        print("\n📝 Testing task creation...")
        test_task = Task(title="Test Task", description="This is a test")
        result = await db.tasks.insert_one(test_task.to_dict())
        print(f"✅ Task created with ID: {result.inserted_id}")
        
        # Test: Read the task
        print("\n📖 Testing task retrieval...")
        retrieved_task = await db.tasks.find_one({"_id": result.inserted_id})
        if retrieved_task:
            print(f"✅ Task retrieved: {retrieved_task['title']}")
        else:
            print("❌ Failed to retrieve task")
            return False
        
        # Test: Update the task
        print("\n✏️  Testing task update...")
        await db.tasks.update_one(
            {"_id": result.inserted_id},
            {"$set": {"completed": True}}
        )
        updated_task = await db.tasks.find_one({"_id": result.inserted_id})
        if updated_task and updated_task.get("completed"):
            print("✅ Task updated successfully")
        else:
            print("❌ Failed to update task")
            return False
        
        # Test: Delete the task
        print("\n🗑️  Testing task deletion...")
        delete_result = await db.tasks.delete_one({"_id": result.inserted_id})
        if delete_result.deleted_count == 1:
            print("✅ Task deleted successfully")
        else:
            print("❌ Failed to delete task")
            return False
        
        # Test: Count all tasks
        print("\n📊 Testing task count...")
        task_count = await db.tasks.count_documents({})
        print(f"✅ Total tasks in database: {task_count}")
        
        print("\n🎉 All tests passed! Your database is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. MongoDB is running (or Atlas connection is correct)")
        print("   2. .env file has correct MONGODB_URL and DB_NAME")
        print("   3. All dependencies are installed (pip install -r requirements.txt)")
        return False
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)

