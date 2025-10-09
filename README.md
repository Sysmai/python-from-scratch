# Python From Scratch

This repository documents my structured journey of learning **Python** from the ground up.
Each phase builds on the last — from small scripts to full-stack APIs with FastAPI and databases.

---

## 📚 Learning Phases

### Phase 1: Core Python Basics

* Small, self-contained programs using loops, conditionals, lists, dicts, functions, and classes.
* **✅ Completed so far | 🟡 In Progress**

  * ✅ `simple_calculator.py` — basic calculator with input validation, loops, and error handling.

  * ✅ `password_generator.py` — secure password generator that uses `secrets` for randomness and customizable options for length, digits, and symbols.

  * ✅ `task_list_manager.py` — CLI task manager built in steps:

    * Step 1: add + list tasks
    * Step 2: mark tasks done, delete tasks
    * Step 3: filter tasks by `done` or `priority`
    * Step 4: JSON save/load for persistence

### Phase 2: FastAPI Intro

* ✅ Installed and configured FastAPI + Uvicorn.
* ✅ Built a simple “Hello World” API with `/hello` and `/greet/{name}` routes.

### Phase 3: CRUD API

* ✅ Create, Read, Update, Delete operations with proper status codes.
* ✅ Start with in-memory data, then expand to persistence.

### Phase 4: Database Integration

* 🟡 Use SQLite with SQLAlchemy ORM.
* 🟡 Deploy to the cloud (Render or AWS Lightsail).

### Phase 5: Advanced Features

* Add pytest testing.
* Use Pydantic for validation.
* Containerize with Docker.
* Optional: simple React frontend.

---

## ✅ Purpose

* Demonstrate **continuous growth in Python skills**.
* Provide **portfolio-ready projects** visible on GitHub.
* Build toward **entry-level Python and full-stack roles**.

---

## 🛠️ Tech Stack

* **Languages:** Python (primary), SQL (SQLite/SQLAlchemy)
* **Frameworks:** FastAPI
* **Tools:** Git, GitHub, Cursor/VS Code, Flake8, Black, Docker (later phases)
* **Deployment:** Render, AWS Lightsail

---

## 📂 Repo Structure

```
python-from-scratch/
│   .gitignore
│   README.md
│
├── phase1_basics/
│   └── simple_calculator.py
│   └── password_generator.py
│   └── task_list_manager.py
│
├── phase2_fastapi/
│   └── hello_world_api.py
│
├── phase3_crud/
│   └── crud_api.py          (coming soon)
│
└── phase4_database/
    └── ...
```

---

## 🔀 Git Usage & Workflow

This repo follows a **commit convention** to keep history clean and professional:

* **feat:** new features or scripts
* **fix:** bug fixes
* **docs:** documentation-only changes
* **refactor:** code improvements without changing behavior

Examples:

```
git commit -m "feat(task-manager): step 2 add mark_done and delete with menu options"
git commit -m "fix(calculator): handle division by zero gracefully"
git commit -m "docs: update README with Phase 1 progress"
```

**Workflow:**

* Work directly on `main` for Phase 1 (small, self-contained scripts).
* Commit in **small increments** (one feature per commit).
* Push updates frequently (`git push`).
* Starting in Phase 2 (FastAPI), feature branches will be used to practice pull-request style merges.

---

## ▶️ How to Run (Phase 1 Scripts)

### Phase 1 Scripts
From the repo root, run with Python 3:

```
python phase1_basics/simple_calculator.py
python phase1_basics/password_generator.py
python phase1_basics/task_list_manager.py
```

* Calculator: simple math operations with input validation.
* Password Generator: generates secure passwords with customizable length/digits/symbols.
* Task List Manager: interactive CLI for adding, listing, filtering, saving, and loading tasks.

### Phase 2 FastAPI App
From the repo root, run with Uvicorn:

```
uvicorn phase2_fastapi.hello_world_api:app --reload
```


Open in browser:
* <http://127.0.0.1:8000/hello>
* <http://127.0.0.1:8000/greet/YourName>
* Docs: <http://127.0.0.1:8000/docs>

### Phase 3 CRUD API

From the repo root, run with Uvicorn:

```
uvicorn phase3_crud.crud_api:app --reload
```

Open in browser:

* [http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks)
* Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → all routes grouped under **Tasks**

---

## 🧩 Endpoints

| Method | Path          | Purpose                 | Body (JSON)                                    | Returns                               |
| :----: | ------------- | ----------------------- | ---------------------------------------------- | ------------------------------------- |
|   GET  | `/tasks`      | List all tasks          | —                                              | `200 OK` + `[{id,title,done}, …]`     |
|   GET  | `/tasks/{id}` | Get one task by ID      | —                                              | `200 OK` + `{id,title,done}` or `404` |
|  POST  | `/tasks`      | Create a task           | `{"title":"...","done":false}` (done optional) | `201 Created` + `{id,title,done}`     |
|  PATCH | `/tasks/{id}` | Update fields (partial) | `{"title":"..."}` or `{"done":true}`           | `200 OK` + updated task or `404`      |
| DELETE | `/tasks/{id}` | Delete a task           | —                                              | `204 No Content` or `404`             |

**Task shape (response model):**

```json
{ "id": 1, "title": "Example", "done": false }
```

---

## ▶️ Quick Tests (Git Bash)

> Use single quotes around JSON to avoid escaping quotes.

### Create

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"First task"}'
```

### List

```bash
curl http://127.0.0.1:8000/tasks
```

### Get One

```bash
curl http://127.0.0.1:8000/tasks/1
```

### Update

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"First task (updated)"}'
```

### Delete

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

---

## 🧪 Manual Test Plan

1. Start server - verify `/docs` loads and shows all “Tasks” routes.
2. POST /tasks - create two tasks; confirm IDs increment (1, 2).
3. GET /tasks - verify both tasks appear.
4. GET /tasks/1 - confirm correct single task returned.
5. PATCH /tasks/1 - change title; verify response reflects update.
6. PATCH /tasks/1 - change `done` to `true`; verify update.
7. DELETE /tasks/1 - confirm response `204 No Content`.
8. GET /tasks/1 - now returns `404 Task not found`.
9. GET /tasks - remaining task still listed.

---

## 🧾 Commit Example

```bash
git add README.md
git commit -m "docs(crud): add Phase 3 usage, endpoints, and manual test plan"
git push origin feature/crud-tasks
```
