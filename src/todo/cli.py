"""
Todo Console Application
Command-line interface
"""

from .service import TodoService


class TodoCLI:
    """Command-line interface for the Todo application."""
    
    def __init__(self):
        """Initialize the CLI with a TodoService."""
        self.service = TodoService()
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*40)
        print("TODO CONSOLE APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("="*40)
    
    def get_user_choice(self):
        """Get and validate user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                if choice in ["1", "2", "3", "4", "5", "6"]:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")
            except KeyboardInterrupt:
                print("\nExiting...")
                return "6"
    
    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title (required): ").strip()
        
        if not title:
            print("Error: Task title is required.")
            return
        
        description = input("Enter task description (optional, press Enter to skip): ").strip()
        
        try:
            task = self.service.add_task(title, description)
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
            print(f"ID: {task.id} | [{status}] | Title: {task.title}")
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
    
    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Console Application!")
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
                print("Thank you for using the Todo Console Application. Goodbye!")
                break
            
            # Pause to let user see the result before showing menu again
            input("\nPress Enter to continue...")