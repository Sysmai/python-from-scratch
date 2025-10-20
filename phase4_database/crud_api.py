"""
Phase 4 - Wire up the database layer
"""
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from .database_orm import (
    get_session,
    init_db,
    orm_list_tasks,
    orm_get_task,
    orm_create_task,
    orm_update_task,
    orm_delete_task,
)


# ------------------------------------------------------
# App and Lifespan
# ------------------------------------------------------
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Initialize the database on startup.
    """
    init_db()
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
    completed: bool = False


class UpdateTask(BaseModel):
    """
    Pydantic model for updating a task.
    """
    title: Optional[str] = None
    completed: Optional[bool] = None


# New: response model for output
class Task(BaseModel):
    """
    Pydantic model for a task.
    """
    id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)


# ------------------------------------------------------
# Routes
# ------------------------------------------------------
@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks(session: Session = Depends(get_session)):
    """Get all tasks"""
    return orm_list_tasks(session)


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int, session: Session = Depends(get_session)):
    """
    Return a single task by its integer ID.
    Raise 404 if not found.
    """

    obj = orm_get_task(session, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@app.post("/tasks", response_model=Task, tags=["Tasks"])
def create_task(payload: CreateTask, session: Session = Depends(get_session)):
    """
    Create a new task with an auto-incremented integer ID.
    """
    return orm_create_task(session, payload.title, None, payload.completed)


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, payload: UpdateTask,
                session: Session = Depends(get_session)):
    """
    Partially update a task. Only fields provided are changed.
    404 if not found.
    400 if body has no updateable fields.
    """
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    obj = orm_update_task(session, task_id, **updates)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Tasks"])
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """
    Delete a task by ID.
    Returns 204 if successful, 404 if not found.
    """
    ok = orm_delete_task(session, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
