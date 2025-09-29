"""Simple CLI Task List Manager
Phase 1, Step 1: Add + List tasks
"""


from typing import List, Dict


Task = Dict[str, object]


def next_id(tasks: List[Task]) -> int:
    """Return the next task ID"""
    if not tasks:
        return 1
    return max(int(t["id"]) for t in tasks) + 1


def add_task(tasks: List[Task], title: str, priority: str = "med") -> Task:
    """Create a new task and append it to tasks."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    task = {
        "id": next_id(tasks),
        "title": title,
        "priority": priority,
        "done": False,
    }
    tasks.append(task)
    return task


def list_tasks(tasks: List[Task]) -> None:
    """List all tasks in the task list."""
    if not tasks:
        print("No tasks yet.")
        return
    print("\nID  |  Title                         | Pri | Done")
    print("-" * 50)
    for t in tasks:
        tid = str(t["id"]).rjust(2)
        title = str(t["title"])[:27].ljust(27)
        pri = str(t["priority"]).rjust(3)
        done = "Yes" if t["done"] else "No"
        print(f"{tid}  |  {title}  |  {pri}  |  {done}")
    print()


def parse_priority(raw: str) -> str:
    """Normalize priority input to 'low', 'med', 'high'."""
    val = raw.strip().lower()
    if val in ["low", "l"]:
        return "low"
    if val in ["medium", "med", "m"]:
        return "med"
    if val in ["high", "h"]:
        return "high"
    return "med"


def find_task_index(tasks: List[Task], task_id: int) -> int | None:
    """Return the index of the task with the given ID, or None if not found."""
    for i, t in enumerate(tasks):
        if int(t["id"]) == task_id:
            return i
    return None


def mark_done(tasks: List[Task], task_id: int) -> bool:
    """Mark a task as done. Return True if successful, False if not found."""
    idx = find_task_index(tasks, task_id)
    if idx is None:
        return False
    tasks[idx]["done"] = True
    return True


def delete_task(tasks: List[Task], task_id: int) -> bool:
    """Delete a task. Return True if successful, False if not found."""
    idx = find_task_index(tasks, task_id)
    if idx is None:
        return False
    del tasks[idx]
    return True


def filter_tasks(
    tasks: List[Task],
    *,
    done: bool | None = None,
    priority: str | None = None,
) -> List[Task]:
    """Filter tasks based on done and priority."""
    out = tasks
    if done is not None:
        out = [t for t in out if bool(t["done"]) is done]
    if priority is not None:
        p = parse_priority(priority)
        out = [t for t in out if str(t["priority"]) == p]
    return out


def list_filtered(tasks: List[Task]) -> None:
    """Prompt user for filters and print result."""
    raw_done = input("Filter by done? (y/n/blank for no filter): "
                     ).strip().lower()
    done_filter = bool | None
    if raw_done in ["y", "yes"]:
        done_filter = True
    elif raw_done in ["n", "no"]:
        done_filter = False
    else:
        done_filter = None

    raw_pri = input("Filter by priority? (low/med/high/blank for no filter): "
                    ).strip()
    pri_filter = parse_priority(raw_pri) if raw_pri else None

    results = filter_tasks(tasks, done=done_filter, priority=pri_filter)
    if not results:
        print("No tasks match the filters.\n")
        return
    list_tasks(results)


def main() -> None:
    """Main function to run the task list manager."""
    tasks: List[Task] = []
    while True:
        print("Task List Manager")
        print("[1] Add Task")
        print("[2] List Tasks")
        print("[3] Mark Done")
        print("[4] Delete Task")
        print("[5] List with Filters")
        print("[6] Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            if not title:
                print("Task title cannot be empty.\n")
                continue
            pri_raw = input("Priority (low/med/high) [med]: ")
            pri = parse_priority(pri_raw if pri_raw else "med")
            try:
                task = add_task(tasks, title, pri)
                print(f"Added task {task['id']}: "
                      f"{task['title']} (pri {task['priority']})\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice == "2":
            list_tasks(tasks)

        elif choice == "3":
            raw = input("Enter task ID to mark done: ").strip()
            if not raw.isdigit():
                print("Please enter a valid task ID.\n")
                continue
            tid = int(raw)
            if mark_done(tasks, tid):
                print(f"Task #{tid} marked done.\n")
            else:
                print(f"No task with ID {tid}.\n")

        elif choice == "4":
            raw = input("Enter task ID to delete: ").strip()
            if not raw.isdigit():
                print("Please enter a valid task ID.\n")
                continue
            tid = int(raw)
            if delete_task(tasks, tid):
                print(f"Task #{tid} deleted.\n")
            else:
                print(f"No task with ID {tid}.\n")

        elif choice == "5":
            list_filtered(tasks)

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Try 1, 2, 3, 4, 5, or 6.\n")


if __name__ == "__main__":
    main()
