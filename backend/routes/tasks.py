"""
Task routes module.
Contains all CRUD endpoints for task management.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from database import get_database
from models import Task
from schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


def convert_objectid_to_str(data: dict) -> dict:
    """
    Convert MongoDB ObjectId to string in dictionary.
    """
    if "_id" in data:
        data["id"] = str(data["_id"])
        del data["_id"]
    return data


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    """
    db = get_database()

    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    result = await db.tasks.insert_one(new_task.to_dict())
    created_task = await db.tasks.find_one({"_id": result.inserted_id})

    if not created_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created task"
        )

    return TaskResponse(**convert_objectid_to_str(created_task))


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks():
    """
    List all tasks.
    """
    db = get_database()
    tasks_cursor = db.tasks.find().sort("created_at", -1)
    tasks = await tasks_cursor.to_list(length=None)

    return [TaskResponse(**convert_objectid_to_str(task)) for task in tasks]


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, data: dict):
    """
    Update only the completed status OR other fields if provided.
    """
    db = get_database()

    try:
        object_id = ObjectId(task_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    update_fields = {}
    if "completed" in data:
        update_fields["completed"] = data["completed"]
    if "title" in data:
        update_fields["title"] = data["title"]
    if "description" in data:
        update_fields["description"] = data["description"]

    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid update fields provided")

    await db.tasks.update_one({"_id": object_id}, {"$set": update_fields})
    updated_task = await db.tasks.find_one({"_id": object_id})
    
    return TaskResponse(**convert_objectid_to_str(updated_task))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """
    Delete a task by ID.
    """
    db = get_database()
    try:
        object_id = ObjectId(task_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await db.tasks.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
