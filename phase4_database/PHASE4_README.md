# `phase4_crud/PHASE4_README.md`

````markdown
# Phase 4: SQLite wiring with plain `sqlite3` (no ORM)

**Goal**
Replace the in-memory list from Phase 3 with real persistence using SQLite and a tiny `database.py` helper layer. Keep the same HTTP contract. No ORM yet.

## How to run
```bash
uvicorn phase4_crud.crud_api:app --reload
````

If the DB file does not exist, `database.py` will create the table on first use.

## Data model

SQLite table schema used in this phase:

```
tasks(
  id          INTEGER PRIMARY KEY,
  title       TEXT NOT NULL,
  description TEXT NULL,
  completed   INTEGER NOT NULL DEFAULT 0
)
```

`completed` is stored as 0 or 1 in SQLite, surfaced as `bool` in the API.

## Pydantic schemas

* **Task**
  `{ id:int, title:str, description:Optional[str], completed:bool }`
* **CreateTask**
  `{ title:str, description:Optional[str], completed:bool=False }`
* **UpdateTask**
  Any subset of `{ title, description, completed }`

## Endpoints and behavior

* `GET /tasks` → `List[Task]`
* `GET /tasks/{id}` → `Task` or 404
* `POST /tasks` → 201 with `Task`
  The route reads the newly created row back and returns it.
* `PATCH /tasks/{id}` → `Task` or 404
  Empty JSON `{}` returns **400** with `{"detail":"No fields provided for update"}`
* `DELETE /tasks/{id}` → 204 or 404

## Route implementation notes

* Each route opens a connection with `with database.connect() as conn:` and closes it automatically when the block exits.
* No FastAPI startup hooks are required for this phase.
* The database layer converts SQLite values to Python types. If you see a mismatch, map values in the route before returning.

## Quick test snippets

```bash
# create
curl -s -X POST http://127.0.0.1:8000/tasks \
  -H "content-type: application/json" \
  -d '{"title":"Write docs","description":"phase 4","completed":false}'

# list
curl -s http://127.0.0.1:8000/tasks

# get by id
curl -s http://127.0.0.1:8000/tasks/1

# patch valid
curl -s -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "content-type: application/json" \
  -d '{"completed":true}'

# patch empty should be 400
curl -i -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "content-type: application/json" \
  -d '{}'

# delete
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

## Persistence checks

1. Create a task.
2. Stop the server.
3. Start it again.
4. `GET /tasks` still shows your task.

## Troubleshooting

* If you see schema mismatches or stale data during development, delete the local DB and let the app recreate it.

  ```bash
  # macOS/Linux
  rm -f tasks.db

  # Windows PowerShell
  Remove-Item -Force tasks.db
  ```
* Ensure `*.db` is ignored by git so you do not commit local data.
