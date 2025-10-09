# ✅ Phase 3 - CRUD API Manual Test Plan

This test plan verifies all Create, Read, Update, and Delete (CRUD) routes for the FastAPI app in `phase3_crud/crud_api.py`.

---

## 🧩 Preconditions

1. Virtual environment active and dependencies installed.
2. Run the API from the repo root:

```bash
uvicorn phase3_crud.crud_api:app --reload
```

3. API available at:
   - Base URL: http://127.0.0.1:8000
   - Docs: http://127.0.0.1:8000/docs

---

## 🚀 Happy Path Tests

| # | Action | Command (Git Bash) | Expected Result |
|---|--------|---------------------|-----------------|
| 1 | Create Task 1 | `curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"First"}'` | Returns 201 Created and JSON `{ "id": 1, "title": "First", "done": false }` |
| 2 | Create Task 2 | `curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"Second"}'` | Returns 201 Created and JSON `{ "id": 2, "title": "Second", "done": false }` |
| 3 | List All | `curl http://127.0.0.1:8000/tasks` | Returns both tasks in a JSON array |
| 4 | Get One (ID 1) | `curl http://127.0.0.1:8000/tasks/1` | Returns `{ "id": 1, "title": "First", "done": false }` |
| 5 | Update Title (ID 1) | `curl -X PATCH http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"title":"First (updated)"}'` | Returns updated JSON with new title |
| 6 | Mark Done (ID 1) | `curl -X PATCH http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'` | Returns `{ "id": 1, "title": "First (updated)", "done": true }` |
| 7 | Delete (ID 1) | `curl -X DELETE http://127.0.0.1:8000/tasks/1` | Returns 204 No Content |
| 8 | Verify Deletion | `curl -i http://127.0.0.1:8000/tasks/1` | Returns 404 Not Found |
| 9 | Check Remaining Tasks | `curl http://127.0.0.1:8000/tasks` | Returns array with only ID 2 |

---

## ⚠️ Negative Tests

| # | Scenario | Command | Expected Result |
|---|----------|---------|-----------------|
| 1 | Update with Empty Body | `curl -i -X PATCH http://127.0.0.1:8000/tasks/2 -H "Content-Type: application/json" -d '{}'` | 400 Bad Request with `{"detail":"No fields to update"}` |
| 2 | Get Missing ID (999) | `curl -i http://127.0.0.1:8000/tasks/999` | 404 Not Found with `{"detail":"Task not found"}` |
| 3 | Delete Missing ID (999) | `curl -i -X DELETE http://127.0.0.1:8000/tasks/999` | 404 Not Found with `{"detail":"Task not found"}` |
| 4 | Wrong Method (POST to /tasks/{id}) | `curl -i -X POST http://127.0.0.1:8000/tasks/2` | 405 Method Not Allowed |

---

## 🧾 Definition of Done

- All happy path and negative tests return expected codes and responses.
- All routes grouped under Tasks in `/docs`.
- All responses follow the `Task` response model (`id`, `title`, `done`).
- No global variables (temporary counter removed).
- README includes usage instructions for Phase 3.
