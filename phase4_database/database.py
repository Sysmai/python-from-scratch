"""
Phase 4, Step 1: Use SQLite with SQLAlchemy ORM
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional


# Store the SQLite file at the repo root as "tasks.db"
DB_PATH = Path("tasks.db")


def get_conn() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database."""
    conn = get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a SQLite row to a dictionary."""
    return {
        "id": int(row["id"]),
        "title": str(row["title"]),
        "description": row["description"],
        "completed": bool(row["completed"])
    }


def list_tasks() -> List[Dict[str, Any]]:
    """List all tasks from the database by id ascending."""
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, title, description, completed FROM tasks ORDER BY id"
        ).fetchall()
        return [row_to_dict(r) for r in rows]
    finally:
        conn.close()


def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Get a task from the database by id."""
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT id, title, description, completed FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return row_to_dict(row) if row else None
    finally:
        conn.close()


def create_task(title: str, description: Optional[str],
                completed: bool) -> Dict[str, Any]:
    """Create a new task in the database."""
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO tasks (title, description, completed) "
            "VALUES (?, ?, ?)",
            (title, description, 1 if completed else 0),
        )
        conn.commit()
        new_id = cur.lastrowid
        return get_task(new_id)  # Fetch and return the newly created record
    finally:
        conn.close()


def update_task(
    task_id: int,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> Optional[Dict[str, Any]]:
    """
    Partially update a task in the database
    and return the updated row as a dict.
    """
    fields = []
    params: List[Any] = []

    if title is not None:
        fields.append("title = ?")
        params.append(title)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if completed is not None:
        fields.append("completed = ?")
        params.append(1 if completed else 0)

    # If no new values were provided, just return the current record
    if not fields:
        return get_task(task_id)

    params.append(task_id)

    conn = get_conn()
    try:
        conn.execute(
            f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?",
            params
        )
        conn.commit()
        return get_task(task_id)
    finally:
        conn.close()


def delete_task(task_id: int) -> bool:
    """Delete a task from the database."""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


if __name__ == "__main__":
    # Quick manual test for the database layer.
    #
    # Run this file directly:
    # python phase4_database/database.py
    #
    # It will:
    # 1. Initialize the DB and create the table if missing.
    # 2. Insert two demo tasks.
    # 3. List all tasks.
    # 4. Update the first task.
    # 5. Delete the second task.
    # 7. List all tasks again.
    print("Initializing database...")
    init_db()

    print("\nCreating two tasks...")
    t1 = create_task("Learn sqlite", "Plain Python first", False)
    t2 = create_task("Wire into API", "FastAPI layer next", False)
    print("Created:", t1)
    print("Created:", t2)

    print("\nListing all tasks:")
    print(list_tasks())

    print("\nMarking first task completed:")
    updated = update_task(t1["id"], completed=True)
    print(updated)

    print("\nDeleting second task:")
    deleted = delete_task(t2["id"])
    print("Deleted:", deleted)

    print("\nFinal list:")
    print(list_tasks())

    print("\nNow stop the script and run it again "
          "(without creating new tasks)")
    print("You should still see the same data - that proves persistence!")
