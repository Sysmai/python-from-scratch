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

* Install and configure FastAPI + Uvicorn.
* Build a simple “Hello World” API.

### Phase 3: CRUD API

* Create, Read, Update, Delete operations with proper status codes.
* Start with in-memory data, then expand to persistence.

### Phase 4: Database Integration

* Use SQLite with SQLAlchemy ORM.
* Deploy to the cloud (Render or AWS Lightsail).

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
│   └── hello_world_api.py   (coming soon)
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

From the repo root, run with Python 3:

```
python phase1_basics/simple_calculator.py
python phase1_basics/password_generator.py
python phase1_basics/task_list_manager.py
```

* Calculator: simple math operations with input validation.
* Password Generator: generates secure passwords with customizable length/digits/symbols.
* Task List Manager: interactive CLI for adding, listing, filtering, saving, and loading tasks.