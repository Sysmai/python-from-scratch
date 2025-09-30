from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI()


# Route: GET /hello
@app.get("/hello")
def read_hello():
    return {"message": "Hello, World!"}


# Route: GET /greet/{name}
@app.get("/greet/{name}")
def read_greet(name: str):
    return {"message": f"Hello, {name}!"}
