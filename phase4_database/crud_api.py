"""
Phase 4 - Wire up the database layer
"""
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from phase4_database import database as db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Initialize the database on startup.
    """
    db.init_db()
    yield


# FastAPI instance
app = FastAPI(
    title="Tasks CRUD API",
    version="0.4.0",
    lifespan=lifespan,
)


# In memory storage for this phase
tasks: List[Dict[str, Any]] = []
# simple ID counter for created tasks
next_id = 1  # pylint: disable=invalid-name


# ------------------------------------------------------
# Models
# ------------------------------------------------------
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
    title: Optional[str] = None
    done: Optional[bool] = None


# New: response model for output
class Task(BaseModel):
    """
    Pydantic model for a task.
    """
    id: int
    title: str
    done: bool


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------
def find_task_index(task_id: int) -> Optional[int]:
    """Return the index of the task with the given ID, or None if not found."""
    for i, t in enumerate(tasks):
        if int(t.get("id", -1)) == int(task_id):
            return i
    return None


def generate_next_id() -> int:
    """Generate a new ID for a task."""
    if not tasks:
        return 1
    return max(int(t.get("id", 0)) for t in tasks) + 1


# ------------------------------------------------------
# Routes
# ------------------------------------------------------
@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks():
    """Get all tasks"""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    """
    Return a single task by its integer ID.
    Raise 404 if not found.
    """

    idx = find_task_index(task_id)
    if idx is not None:
        return tasks[idx]
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task,
          tags=["Tasks"])
def create_task(payload: CreateTask):
    """
    Create a new task with an auto-incremented integer ID.
    """
    task = {
        "id": generate_next_id(),
        "title": payload.title,
        "done": payload.done,
    }
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, payload: UpdateTask):
    """
    Partially update a task. Only fields provided are changed.
    404 if not found.
    400 if body has no updateable fields.
    """
    # find the task
    idx = find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # at least one field must be provided
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="No fields to update")

    # update the task
    if payload.title is not None:
        tasks[idx]["title"] = payload.title

    if payload.done is not None:
        tasks[idx]["done"] = payload.done

    return tasks[idx]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task by ID.
    Returns 204 if successful, 404 if not found.
    """
    idx = find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # delete the task
    tasks.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
