"""
Todo Console Application - Advanced Level
Command-line interface with recurring, due dates, and reminders
"""

from service import TodoService
from models import RecurrencePattern
from datetime import datetime


class TodoCLI:
    """Command-line interface for the Todo application with advanced features."""

    def __init__(self):
        """Initialize the CLI with a TodoService."""
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("TODO CONSOLE APPLICATION - ADVANCED LEVEL")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Set Task as Recurring")
        print("7. Set Due Date for Task")
        print("8. Set Reminder for Task")
        print("9. View Overdue Tasks")
        print("10. View Tasks Due Soon")
        print("11. Exit")
        print("="*50)

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
        from models import Priority
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)

        # Get due date
        due_date_input = input("Enter due date (YYYY-MM-DD HH:MM, optional, press Enter to skip): ").strip()
        due_date = None
        if due_date_input:
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD HH:MM format.")
                return

        # Get if recurring
        is_recurring_input = input("Is this task recurring? (y/n, default is n): ").strip().lower()
        is_recurring = is_recurring_input == 'y'
        
        recurrence_pattern = None
        if is_recurring:
            print("Select recurrence pattern (1: Daily, 2: Weekly, 3: Monthly): ")
            pattern_choice = input("Enter choice (1-3): ").strip()
            pattern_map = {"1": RecurrencePattern.DAILY, "2": RecurrencePattern.WEEKLY, "3": RecurrencePattern.MONTHLY}
            if pattern_choice in pattern_map:
                recurrence_pattern = pattern_map[pattern_choice]
            else:
                print("Invalid pattern choice. Task will not be recurring.")
                is_recurring = False

        # Get if has reminder
        has_reminder_input = input("Enable reminder for this task? (y/n, default is n): ").strip().lower()
        has_reminder = has_reminder_input == 'y'

        try:
            task = self.service.add_task(
                title, description, priority, 
                due_date=due_date, 
                is_recurring=is_recurring, 
                recurrence_pattern=recurrence_pattern,
                has_reminder=has_reminder
            )
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
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
            recurring_info = f" | Recurring: {task.recurrence_pattern.value}" if task.is_recurring else ""
            due_info = f" | Due: {task.due_date}" if task.due_date else ""
            reminder_info = f" | Reminder: ON" if task.has_reminder else ""
            print(f"ID: {task.id} | [{status}] | Title: {task.title} | Priority: {task.priority.value}{recurring_info}{due_info}{reminder_info}")
            if task.description:
                print(f"     Description: {task.description}")
            if task.tags:
                print(f"     Tags: {', '.join(task.tags)}")
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

    def set_task_recurring(self):
        """Handle setting a task as recurring."""
        print("\n--- Set Task as Recurring ---")
        
        try:
            task_id = int(input("Enter task ID to set as recurring: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print("Select recurrence pattern (1: Daily, 2: Weekly, 3: Monthly): ")
        pattern_choice = input("Enter choice (1-3): ").strip()
        pattern_map = {"1": RecurrencePattern.DAILY, "2": RecurrencePattern.WEEKLY, "3": RecurrencePattern.MONTHLY}
        
        if pattern_choice in pattern_map:
            recurrence_pattern = pattern_map[pattern_choice]
            task.is_recurring = True
            task.recurrence_pattern = recurrence_pattern
            print(f"Task {task_id} set to recurring ({recurrence_pattern.value} pattern)!")
        else:
            print("Error: Invalid pattern choice. Please enter 1, 2, or 3.")

    def set_due_date(self):
        """Handle setting a due date for a task."""
        print("\n--- Set Due Date for Task ---")

        try:
            task_id = int(input("Enter task ID to set due date: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        due_date_input = input("Enter due date (YYYY-MM-DD HH:MM): ").strip()
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M")
            updated_task = self.service.set_task_due_date(task_id, due_date)
            if updated_task:
                print(f"Due date set for task {task_id} successfully! Due: {updated_task.due_date}")
            else:
                print("Error: Due date could not be set for the task.")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD HH:MM format.")

    def set_reminder(self):
        """Handle enabling a reminder for a task."""
        print("\n--- Set Reminder for Task ---")

        try:
            task_id = int(input("Enter task ID to enable reminder: ").strip())
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        if not task.due_date:
            print(f"Error: Task with ID {task_id} has no due date. Set a due date first.")
            return

        updated_task = self.service.enable_task_reminder(task_id)
        if updated_task:
            print(f"Reminder enabled for task {task_id} successfully!")
            print(f"Reminder will trigger at: {updated_task.due_date}")
        else:
            print("Error: Reminder could not be enabled for the task.")

    def view_overdue_tasks(self):
        """Handle viewing overdue tasks."""
        print("\n--- Overdue Tasks ---")
        overdue_tasks = self.service.get_overdue_tasks()

        if not overdue_tasks:
            print("No overdue tasks found.")
            return

        for task in overdue_tasks:
            print(f"ID: {task.id} | Title: {task.title} | Due: {task.due_date}")
            if task.description:
                print(f"     Description: {task.description}")
            print()

    def view_tasks_due_soon(self):
        """Handle viewing tasks due soon."""
        print("\n--- Tasks Due Soon ---")
        
        try:
            hours = int(input("Enter number of hours ahead to check (default 24): ").strip() or "24")
        except ValueError:
            print("Error: Invalid number. Using default value of 24 hours.")
            hours = 24

        due_soon_tasks = self.service.get_tasks_due_soon(hours)

        if not due_soon_tasks:
            print(f"No tasks due within the next {hours} hours.")
            return

        for task in due_soon_tasks:
            print(f"ID: {task.id} | Title: {task.title} | Due: {task.due_date}")
            if task.description:
                print(f"     Description: {task.description}")
            print()

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Console Application - Advanced Level!")
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
                self.set_task_recurring()
            elif choice == "7":
                self.set_due_date()
            elif choice == "8":
                self.set_reminder()
            elif choice == "9":
                self.view_overdue_tasks()
            elif choice == "10":
                self.view_tasks_due_soon()
            elif choice == "11":
                print("Thank you for using the Todo Console Application. Goodbye!")
                break

            # Pause to let user see the result before showing menu again
            input("\nPress Enter to continue...")