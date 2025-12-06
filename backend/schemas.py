from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    """
    Schema for incoming task creation requests from the frontend.
    """
    title: str
    description: Optional[str] = ""
    completed: bool = False


class TaskResponse(TaskCreate):
    """
    Schema for outgoing task responses sent to the frontend.
    Includes MongoDB `_id` converted to string.
    """
    id: str
