"""
Phase 4, ORM: SQLAlchemy setup and Task model
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional, Generator

from sqlalchemy import Boolean, Integer, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

# Store the SQLite file at the repo root as "tasks.db"
DB_PATH = Path(__file__).resolve().parent / "tasks.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine: manages DB connections.
engine = create_engine(
    DATABASE_URL,
    echo=False,  # set to True temporarily to see SQL written to the console
    future=True,
    connect_args={"check_same_thread": False},
)


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


class Task(Base):
    """
    ORM model for the tasks table.
    Columns mirror the prior sqlite3 version.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(
        String, default="", nullable=False)
    completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)


# Session factory: creates Session objects for DB interactions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def init_db() -> None:
    """Create tables if missing."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Transaction scope: commit on success, rollback on error,
    and always close the session.
    """

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def orm_list_tasks(session: Session) -> List[Task]:
    """List all tasks from the database."""
    result = session.execute(select(Task).order_by(Task.id))
    return list(result.scalars())


def orm_get_task(session: Session, task_id: int) -> Optional[Task]:
    """Get a task by id."""
    return session.get(Task, task_id)


def orm_create_task(
    session: Session,
    title: str,
    description: Optional[str],
    completed: bool,
) -> Task:
    """Create a new task."""
    task = Task(
        title=title,
        description=description or "",
        completed=completed
    )
    session.add(task)
    session.flush()  # assign autoincrement id before commit
    return task


def orm_update_task(
    session: Session,
    task_id: int,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> Optional[Task]:
    """Partially update a task and return the updated ORM object."""
    task = session.get(Task, task_id)
    if not task:
        return None
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed
    session.flush()
    return task


def orm_delete_task(session: Session, task_id: int) -> bool:
    """Delete a task from the database."""
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.flush()
    return True


if __name__ == "__main__":
    # Quick manual test for the ORM layer.
    # Run:
    # python -m phase4_database.database_orm
    print("Initializing ORM database...")
    init_db()

    with session_scope() as s:
        print("\nCreating two tasks...")
        t1 = orm_create_task(
            s,
            "Learn ORM",
            "Replace sqlite3 with SQLAlchemy",
            False
            )
        t2 = orm_create_task(
            s,
            "Wire into API",
            "FastAPI layer next",
            False)
        print("Created:", {"id": t1.id, "title": t1.title,
                           "description": t1.description,
                           "completed": t1.completed})
        print("Created:", {"id": t2.id, "title": t2.title,
                           "description": t2.description,
                           "completed": t2.completed})

    # List all tasks
    with session_scope() as s:
        print("\nListing all tasks:")
        for t in orm_list_tasks(s):
            print({"id": t.id, "title": t.title, "completed": t.completed})

    # Update
    with session_scope() as s:
        print("\nMarking first task completed:")
        updated = orm_update_task(s, t1.id, completed=True)
        if updated is None:
            print("Update failed: no task found for id", t1.id)
        else:
            print("Updated:", {"id": updated.id, "title": updated.title,
                               "completed": updated.completed})

    # Delete
    with session_scope() as s:
        print("\nDeleting second task:")
        deleted = orm_delete_task(s, t2.id)
        print("Deleted:", deleted)

    # List all tasks
    with session_scope() as s:
        print("\nFinal list:")
        for t in orm_list_tasks(s):
            print({"id": t.id, "title": t.title, "completed": t.completed})

    print("\nRe-run to confirm persistence:")
