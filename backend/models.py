"""
Database models for MongoDB collections.
Defines the structure of documents stored in MongoDB.
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId


class Task:
    """
    Task model representing a task document in MongoDB.
    This is a simple class to structure task data.
    """
    
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        """
        Initialize a Task instance.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            completed: Completion status (default: False)
            created_at: Creation timestamp (default: current time)
            _id: MongoDB ObjectId (optional, auto-generated if not provided)
        """
        self._id = _id or ObjectId()
        self.title = title
        self.description = description or ""
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """
        Convert Task instance to dictionary for MongoDB storage.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Create Task instance from MongoDB document dictionary.
        
        Args:
            data: Dictionary containing task data from MongoDB
            
        Returns:
            Task instance
        """
        return cls(
            _id=data.get("_id"),
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=data.get("created_at", datetime.utcnow())
        )

