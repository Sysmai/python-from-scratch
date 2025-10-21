# Phase 4: Database Layer with SQLAlchemy ORM

**Goal**
Replace the in-memory list from Phase 3 with persistent storage using **SQLite + SQLAlchemy ORM**, while keeping the same FastAPI endpoints and data models.

---

## How to run

```bash
uvicorn phase4_database.crud_api:app --reload
````

If the database file does not exist, it will be automatically created by SQLAlchemy on first use.

---

## Data model

SQLAlchemy ORM model (`Task`) used in this phase:

| Column        | Type              | Description          |
| ------------- | ----------------- | -------------------- |
| `id`          | Integer           | Primary key          |
| `title`       | String            | Required task title  |
| `description` | String (nullable) | Optional description |
| `completed`   | Boolean           | Defaults to `False`  |

Example record:

```json
{ "id": 1, "title": "Example Task", "description": null, "completed": false }
```

---

## Pydantic schemas

* **Task**
  `{ id:int, title:str, description:Optional[str], completed:bool }`

* **CreateTask**
  `{ title:str, description:Optional[str], completed:bool=False }`

* **UpdateTask**
  Any subset of `{ title, description, completed }`

---

## Endpoints and behavior

| Method   | Route         | Description                                |
| -------- | ------------- | ------------------------------------------ |
| `GET`    | `/tasks`      | Return all tasks (empty list if none)      |
| `GET`    | `/tasks/{id}` | Return task by ID or 404                   |
| `POST`   | `/tasks`      | Create new task, return created record     |
| `PATCH`  | `/tasks/{id}` | Update partial fields, return updated task |
| `DELETE` | `/tasks/{id}` | Delete by ID, return 204 or 404            |

All routes now depend on a database `Session` injected with `Depends(get_session)` from `database_orm.py`.

---

## Implementation notes

* The ORM model and engine are defined in `database_orm.py`.
* FastAPI routes live in `crud_api.py` and interact directly with ORM helpers.
* There is **no direct SQLite connection code** anymore - SQLAlchemy manages everything.
* The boolean field `completed` is now consistent across models and the database.
* `database_orm.py` fully replaces the old `database.py` used earlier.

---

## Quick test snippets

```bash
# create
curl -s -X POST http://127.0.0.1:8000/tasks \
  -H "content-type: application/json" \
  -d '{"title":"Write docs","description":"Finalize Phase 4","completed":false}'

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

---

## Persistence checks

1. Create a task.
2. Stop the server.
3. Start it again.
4. `GET /tasks` still shows your task.

This confirms that ORM persistence is working correctly.

---

## Troubleshooting

* If you see schema mismatches or validation errors, delete the local `tasks.db` and let the ORM recreate it:

  ```bash
  # macOS/Linux
  rm -f phase4_database/tasks.db

  # Windows PowerShell
  Remove-Item -Force phase4_database/tasks.db
  ```
* Ensure your `.gitignore` includes:

  ```
  *.db
  *.db-journal
  ```

  so you don’t accidentally commit local database files.
