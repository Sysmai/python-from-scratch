# Python From Scratch

This repository documents my structured journey of learning **Python** from the ground up.
Each phase builds on the last — from small scripts to full-stack APIs with FastAPI and databases.

---

## 📚 Learning Phases

### Phase 1: Core Python Basics

* Small, self-contained programs using loops, conditionals, lists, dicts, functions, and classes.
* **✅ Completed so far | 🟡 In Progress**

  * ✅ `simple_calculator.py` — basic calculator with input validation, loops, and error handling.

  * ✅ `password_generator.py` — a simple password generator that uses secure randomness and
                                 customizable options for length, digits, and symbols.

  * 🟡 `task_list_manager.py` — a CLI app that tracks tasks in memory using lists, dicts, functions,
                                 string parsing, etc...

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
|
├── phase2_fastapi/
│   └── hello_world_api.py   (coming soon)
│
├── phase3_crud/
│   └── crud_api.py          (coming soon)
│
└── phase4_database/
    └── ...
```