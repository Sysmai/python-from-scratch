"""
Phase 4 - Wire up the database layer
"""
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from phase4_database import database as db


# ------------------------------------------------------
# App and Lifespan
# ------------------------------------------------------
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
# Helpers (Phase 4, database version)
# ------------------------------------------------------
def _to_api_task(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a database record to an API task."""
    return {
        "id": int(rec["id"]),
        "title": str(rec["title"]),
        "done": bool(rec["completed"]),
    }


# ------------------------------------------------------
# Routes
# ------------------------------------------------------
@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks():
    """Get all tasks"""
    rows = db.list_tasks()
    return [_to_api_task(r) for r in rows]


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    """
    Return a single task by its integer ID.
    Raise 404 if not found.
    """

    rec = db.get_task(task_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Task not found")
    return _to_api_task(rec)


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task,
          tags=["Tasks"])
def create_task(payload: CreateTask):
    """
    Create a new task with an auto-incremented integer ID.
    """
    rec = db.create_task(
        title=payload.title,
        description=None,
        completed=payload.done,
    )
    return _to_api_task(rec)


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, payload: UpdateTask):
    """
    Partially update a task. Only fields provided are changed.
    404 if not found.
    400 if body has no updateable fields.
    """
    rec = db.update_task(
        task_id,
        title=payload.title,
        description=None,  # unchanged in this API
        completed=(payload.done if payload.done is not None else None),
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Task not found")
    return _to_api_task(rec)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task by ID.
    Returns 204 if successful, 404 if not found.
    """
    ok = db.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
