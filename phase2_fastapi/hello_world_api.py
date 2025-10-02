"""Simple FastAPI "Hello World" API
Phase 2, Step 1: Create a simple API with two routes
"""

from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI()


# Route: GET /hello
@app.get("/hello")
def read_hello():
    """Return a simple "Hello, World!" message."""
    return {"message": "Hello, World!"}


# Route: GET /greet/{name}
@app.get("/greet/{name}")
def read_greet(name: str):
    """Return a personalized "Hello, {name}!" message."""
    return {"message": f"Hello, {name}!"}
