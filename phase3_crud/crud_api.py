"""
Phase 3, Step 1: Create a CRUD API with FastAPI
"""
from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi import HTTPException


app = FastAPI()


# In memory storage for this phase
tasks: List[Dict[str, Any]] = []


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
