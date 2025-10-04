"""
Phase 3, Step 1: Create a CRUD API with FastAPI
"""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field


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


class UpdateTask(BaseModel):
    """
    Pydantic model for updating a task.
    """
    title: Optional[str] = Field(default=None)
    done: Optional[bool] = Field(default=None)


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


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, payload: UpdateTask):
    """
    Partially update a task. Only fields provided are changed.
    404 if not found.
    400 if body has no updateable fields.
    """
    # find the task
    for t in tasks:
        if t in tasks:
            if t.get("id") == task_id:
                # at least one field must be provided
                if payload.title is None and payload.done is None:
                    raise HTTPException(status_code=400,
                                        detail="No fields to update")
                if payload.title is not None:
                    t["title"] = payload.title
                if payload.done is not None:
                    t["done"] = payload.done
                return t
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """
    Delete a task by ID.
    Returns 204 if successful, 404 if not found.
    """
    for i, t in enumerate(tasks):
        if t.get("id") == task_id:
            tasks.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Task not found")
