"""
Phase 3, Step 1: Create a CRUD API with FastAPI
"""
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


# In memory storage for this phase
tasks: List[Dict[str, Any]] = []
# simple ID counter for created tasks
next_id = 1  # pylint: disable=invalid-name


class CreateTask(BaseModel):
    """
    Pydantic model for creating a new task.
    """
    title: str
    done: bool = False


@app.get("/tasks")
def get_tasks():
    """Get all tasks"""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """
    Return a single task by its integer ID.
    Raise 404 if not found.
    """

    # naive linear search (fine for in-memory lists)
    for t in tasks:
        if t.get("id") == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask):
    """
    Create a new task with an auto-incremented integer ID.
    """
    global next_id  # temporary global variable
    task = {
        "id": next_id,
        "title": payload.title,
        "done": payload.done,
    }
    tasks.append(task)
    next_id += 1
    return task
