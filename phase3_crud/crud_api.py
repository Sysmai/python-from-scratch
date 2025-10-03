"""
Phase 3, Step 1: Create a CRUD API with FastAPI
"""
from typing import List, Dict, Any
from fastapi import FastAPI


app = FastAPI()


# In memory storage for this phase
tasks: List[Dict[str, Any]] = []


@app.get("/tasks")
def get_tasks():
    """Get all tasks"""
    return tasks
