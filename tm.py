
import json
import os
from datetime import datetime


class Task:
    """Represents a single task in our application."""
    
    # Allowed values for validation
    ALLOWED_PRIORITIES = ["Low", "Medium", "High"]
    ALLOWED_STATUSES = ["Pending", "In Progress", "Completed"]

    def __init__(self, task_id, title, priority, due_date, status="Pending"):
        self.task_id = task_id
        self.title = self.validate_title(title)
        self.priority = self.validate_priority(priority)
        self.due_date = self.validate_date(due_date)
        self.status = self.validate_status(status)

    def validate_title(self, title):
        """Make sure title is not empty."""
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Task title cannot be empty!")
        return clean_title

    def validate_priority(self, priority):
        """Check if priority is Low, Medium, or High."""
        formatted = priority.strip().title()
        if formatted not in self.ALLOWED_PRIORITIES:
            raise ValueError(f"Invalid priority! Choose from: {', '.join(self.ALLOWED_PRIORITIES)}")
        return formatted

    def validate_date(self, date_str):
        """Make sure date format is YYYY-MM-DD."""
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date '{date_str}'. Please use YYYY-MM-DD format.")

    def validate_status(self, status):
        """Check if status is valid."""
        formatted = status.strip().title()
        if formatted not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid status! Choose from: {', '.join(self.ALLOWED_STATUSES)}")
        return formatted

    def is_overdue(self):
        """Check if today's date is past the due date (only for unfinished tasks)."""
        if self.status == "Completed":
            return False
        today_str = datetime.now().strftime("%Y-%m-%d")
        return self.due_date < today_str

    def to_dict(self):
        """Convert task object to dictionary for JSON saving."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from dictionary loaded from JSON."""
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            priority=data["priority"],
            due_date=data["due_date"],
            status=data["status"]
        )


class TaskManager:
    """Manages the list of tasks and handles saving/loading to JSON."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_from_file()

    def generate_id(self):
        """Generates a unique ID for each task."""
        current = self.next_id
        self.next_id += 1
        return current

    def add_task(self, title, priority, due_date):
        """Adds a new task to the list and saves to file."""
        new_id = self.generate_id()
        task = Task(new_id, title, priority, due_date)
        self.tasks.append(task)
        self.save_to_file()
        return task

    def update_status(self, task_id, new_status):
        """Finds a task by ID and updates its status."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = task.validate_status(new_status)
                self.save_to_file()
                return True
        return False

    def delete_task(self, task_id):
        """Removes a task by ID if it exists."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                self.save_to_file()
                return True
        return False

    def get_all_tasks(self):
        """Returns all tasks sorted by due date."""
        return sorted(self.tasks, key=lambda t: t.due_date)

    def search_and_filter(self, keyword=None, priority=None, status=None):
        """Filters tasks by keyword, priority, or status."""
        filtered_list = self.tasks

        if keyword:
            filtered_list = [t for t in filtered_list if keyword.lower() in t.title.lower()]

        if priority:
            formatted_p = priority.strip().title()
            filtered_list = [t for t in filtered_list if t.priority == formatted_p]

        if status:
            formatted_s = status.strip().title()
            filtered_list = [t for t in filtered_list if t.status == formatted_s]

        return sorted(filtered_list, key=lambda t: t.due_date)

    def get_summary(self):
        """Calculates total counts for status report."""
        total = len(self.tasks)
        pending = 0
        in_progress = 0
        completed = 0
        overdue = 0

        for t in self.tasks:
            if t.status == "Pending":
                pending += 1
            elif t.status == "In Progress":
                in_progress += 1
            elif t.status == "Completed":
                completed += 1
            
            if t.is_overdue():
                overdue += 1

        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "overdue": overdue
        }

    def save_to_file(self):
        """Saves current tasks and next_id to JSON."""
        try:
            dict_tasks = [t.to_dict() for t in self.tasks]
            data = {
                "next_id": self.next_id,
                "tasks": dict_tasks
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self):
        """Loads task list from JSON file if it exists."""
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.next_id = data.get("next_id", 1)
                task_dicts = data.get("tasks", [])
                self.tasks = [Task.from_dict(d) for d in task_dicts]
        except Exception as e:
            print(f"Warning: Could not load existing file ({e}). Starting fresh.")
            self.tasks = []
            self.next_id = 1


def show_menu():
    """Prints the CLI options."""
    print("\n----------------------------------")
    print("      TASK MANAGEMENT CONSOLE     ")
    print("----------------------------------")
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. Search & Filter Tasks")
    print("4. Update Task Status")
    print("5. Delete Task")
    print("6. View Summary Report")
    print("7. Exit")
    print("----------------------------------")


def display_task_table(task_list):
    """Prints tasks nicely in terminal."""
    if not task_list:
        print("No tasks found.")
        return

    print(f"\n{'ID':<5} | {'Priority':<8} | {'Status':<12} | {'Due Date':<10} | {'Overdue?':<8} | {'Title'}")
    print("-" * 75)
    for t in task_list:
        overdue_str = "YES" if t.is_overdue() else "No"
        print(f"{t.task_id:<5} | {t.priority:<8} | {t.status:<12} | {t.due_date:<10} | {overdue_str:<8} | {t.title}")


def main():
    manager = TaskManager()

    while True:
        show_menu()
        choice = input("Enter option (1-7): ").strip()

        if choice == '1':
            print("\n--- Add Task ---")
            title = input("Enter Title: ")
            priority = input("Enter Priority (Low/Medium/High): ")
            due_date = input("Enter Due Date (YYYY-MM-DD): ")

            try:
                task = manager.add_task(title, priority, due_date)
                print(f"[SUCCESS] Task #{task.task_id} added successfully!")
            except ValueError as error:
                print(f"[ERROR] {error}")

        elif choice == '2':
            print("\n--- All Tasks ---")
            display_task_table(manager.get_all_tasks())

        elif choice == '3':
            print("\n--- Search & Filter ---")
            kw = input("Keyword search (Press Enter to skip): ").strip() or None
            p = input("Filter Priority (Low/Medium/High or Enter to skip): ").strip() or None
            s = input("Filter Status (Pending/In Progress/Completed or Enter to skip): ").strip() or None

            results = manager.search_and_filter(keyword=kw, priority=p, status=s)
            print(f"\nMatching Results ({len(results)} found):")
            display_task_table(results)

        elif choice == '4':
            print("\n--- Update Status ---")
            try:
                t_id = int(input("Enter Task ID: "))
                new_status = input("Enter New Status (Pending/In Progress/Completed): ")
                
                if manager.update_status(t_id, new_status):
                    print(f"[SUCCESS] Updated status for Task #{t_id}.")
                else:
                    print(f"[ERROR] Task ID #{t_id} not found.")
            except ValueError:
                print("[ERROR] Invalid input! ID must be a number.")

        elif choice == '5':
            print("\n--- Delete Task ---")
            try:
                t_id = int(input("Enter Task ID to delete: "))
                if manager.delete_task(t_id):
                    print(f"[SUCCESS] Task #{t_id} deleted successfully.")
                else:
                    print(f"[ERROR] Task ID #{t_id} not found.")
            except ValueError:
                print("[ERROR] Please enter a valid numerical ID.")

        elif choice == '6':
            print("\n--- Summary Report ---")
            report = manager.get_summary()
            print(f"Total Tasks:   {report['total']}")
            print(f"Pending:       {report['pending']}")
            print(f"In Progress:   {report['in_progress']}")
            print(f"Completed:     {report['completed']}")
            print(f"Overdue Tasks: {report['overdue']}")

        elif choice == '7':
            print("\nExiting Task Management Console. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()