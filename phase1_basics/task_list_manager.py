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


def main() -> None:
    """Main function to run the task list manager."""
    tasks: List[Task] = []
    while True:
        print("Task List Manager")
        print("[1] Add Task")
        print("[2] List Tasks")
        print("[3] Quit")
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
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Try 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
