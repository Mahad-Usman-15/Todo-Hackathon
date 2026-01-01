"""
Todo Console Application - Intermediate Level
Command-line interface with enhanced features
"""

from service import TodoService
from models import Priority


class TodoCLI:
    """Command-line interface for the Todo application with enhanced features."""

    def __init__(self):
        """Initialize the CLI with a TodoService."""
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*40)
        print("TODO CONSOLE APPLICATION - INTERMEDIATE LEVEL")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Set Task Priority")
        print("7. Add Tag to Task")
        print("8. Search Tasks")
        print("9. Filter Tasks")
        print("10. Sort Tasks")
        print("11. Exit")
        print("="*40)

    def get_user_choice(self):
        """Get and validate user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-11): ").strip()
                if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 11.")
            except KeyboardInterrupt:
                print("\nExiting...")
                return "11"

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title (required): ").strip()

        if not title:
            print("Error: Task title is required.")
            return

        description = input("Enter task description (optional, press Enter to skip): ").strip()
        
        # Get priority
        print("Select priority (1: High, 2: Medium, 3: Low): ")
        priority_choice = input("Enter choice (1-3, default is 2): ").strip()
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)

        try:
            task = self.service.add_task(title, description, priority=priority)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}, Priority: {task.priority.value}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- Task List ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            tags_str = f" | Tags: {', '.join(task.tags) if task.tags else 'None'}"
            print(f"ID: {task.id} | [{status}] | Title: {task.title} | Priority: {task.priority.value}{tags_str}")
            if task.description:
                print(f"     Description: {task.description}")
            print()

    def update_task(self):
        """Handle updating an existing task."""
        print("\n--- Update Task ---")

        try:
            task_id = int(input("Enter task ID to update: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: ID: {task.id}, Title: {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
        new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

        # Use None to indicate no change, otherwise use the new value
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        try:
            updated_task = self.service.update_task(task_id, title_to_update, description_to_update)
            if updated_task:
                print(f"Task updated successfully! ID: {updated_task.id}, Title: {updated_task.title}")
            else:
                print("Error: Task could not be updated.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")

        try:
            task_id = int(input("Enter task ID to delete: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        success = self.service.delete_task(task_id)
        if success:
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def toggle_task_status(self):
        """Handle toggling a task's completion status."""
        print("\n--- Toggle Task Status ---")

        try:
            task_id = int(input("Enter task ID to toggle: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        status_before = "Complete" if task.completed else "Incomplete"
        updated_task = self.service.toggle_task_status(task_id)
        status_after = "Complete" if updated_task.completed else "Incomplete"

        print(f"Task status toggled! ID: {updated_task.id}, Title: {updated_task.title}")
        print(f"Status changed from '{status_before}' to '{status_after}'.")

    def set_task_priority(self):
        """Handle setting task priority."""
        print("\n--- Set Task Priority ---")
        
        try:
            task_id = int(input("Enter task ID to update priority: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print("Select priority (1: High, 2: Medium, 3: Low): ")
        priority_choice = input("Enter choice (1-3): ").strip()
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
        
        if priority_choice in priority_map:
            priority = priority_map[priority_choice]
            updated_task = self.service.update_task_priority(task_id, priority)
            if updated_task:
                print(f"Priority updated successfully! ID: {updated_task.id}, Title: {updated_task.title}, Priority: {updated_task.priority.value}")
            else:
                print("Error: Task priority could not be updated.")
        else:
            print("Error: Invalid priority choice. Please enter 1, 2, or 3.")

    def add_tag_to_task(self):
        """Handle adding a tag to a task."""
        print("\n--- Add Tag to Task ---")

        try:
            task_id = int(input("Enter task ID to add tag: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        tag = input("Enter tag to add: ").strip()
        if not tag:
            print("Error: Tag cannot be empty.")
            return

        updated_task = self.service.add_tag_to_task(task_id, tag)
        if updated_task:
            print(f"Tag '{tag}' added to task {task_id} successfully!")
            print(f"Current tags: {', '.join(updated_task.tags) if updated_task.tags else 'None'}")
        else:
            print("Error: Tag could not be added to the task.")

    def search_tasks(self):
        """Handle searching tasks."""
        print("\n--- Search Tasks ---")
        search_term = input("Enter search term: ").strip()

        if not search_term:
            print("Error: Search term cannot be empty.")
            return

        tasks = self.service.search_tasks(search_term)

        if tasks:
            print(f"Found {len(tasks)} matching tasks:")
            for task in tasks:
                status = "Complete" if task.completed else "Incomplete"
                print(f"ID: {task.id} | [{status}] | Title: {task.title} | Priority: {task.priority.value}")
                if task.description:
                    print(f"     Description: {task.description}")
                print()
        else:
            print("No tasks found matching the search term.")

    def filter_tasks(self):
        """Handle filtering tasks."""
        print("\n--- Filter Tasks ---")
        
        # Get filter options
        print("Filter by completion status (1: Complete, 2: Incomplete, 3: Any): ")
        status_choice = input("Enter choice (1-3, press Enter for Any): ").strip()
        status_map = {"1": True, "2": False}
        status = status_map.get(status_choice, None)
        
        print("Filter by priority (1: High, 2: Medium, 3: Low, 4: Any): ")
        priority_choice = input("Enter choice (1-4, press Enter for Any): ").strip()
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
        priority = priority_map.get(priority_choice, None)
        
        tag_input = input("Filter by tag (press Enter to skip): ").strip()
        tags = {tag_input} if tag_input else None

        # Apply filters
        tasks = self.service.filter_tasks(status=status, priority=priority, tags=tags)

        if tasks:
            print(f"Found {len(tasks)} matching tasks:")
            for task in tasks:
                status = "Complete" if task.completed else "Incomplete"
                print(f"ID: {task.id} | [{status}] | Title: {task.title} | Priority: {task.priority.value}")
                if task.tags:
                    print(f"     Tags: {', '.join(task.tags)}")
                if task.description:
                    print(f"     Description: {task.description}")
                print()
        else:
            print("No tasks found matching the filter criteria.")

    def sort_tasks(self):
        """Handle sorting tasks."""
        print("\n--- Sort Tasks ---")
        
        print("Sort by (1: Title, 2: Priority, 3: Due Date, 4: ID): ")
        sort_choice = input("Enter choice (1-4, default is 4): ").strip()
        sort_map = {"1": "title", "2": "priority", "3": "due_date", "4": "id"}
        sort_by = sort_map.get(sort_choice, "id")
        
        print("Sort order (1: Ascending, 2: Descending): ")
        order_choice = input("Enter choice (1-2, default is 1): ").strip()
        ascending = order_choice != "2"

        tasks = self.service.sort_tasks(sort_by=sort_by, ascending=ascending)

        if tasks:
            print(f"Tasks sorted by {sort_by} ({'ascending' if ascending else 'descending'}):")
            for task in tasks:
                status = "Complete" if task.completed else "Incomplete"
                print(f"ID: {task.id} | [{status}] | Title: {task.title} | Priority: {task.priority.value}")
                if task.tags:
                    print(f"     Tags: {', '.join(task.tags)}")
                if task.description:
                    print(f"     Description: {task.description}")
                print()
        else:
            print("No tasks to display.")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Console Application - Intermediate Level!")
        print("This application stores tasks in memory only. All data will be lost when the application exits.")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_task_status()
            elif choice == "6":
                self.set_task_priority()
            elif choice == "7":
                self.add_tag_to_task()
            elif choice == "8":
                self.search_tasks()
            elif choice == "9":
                self.filter_tasks()
            elif choice == "10":
                self.sort_tasks()
            elif choice == "11":
                print("Thank you for using the Todo Console Application. Goodbye!")
                break

            # Pause to let user see the result before showing menu again
            input("\nPress Enter to continue...")