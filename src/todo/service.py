"""
Todo Console Application
Business logic layer
"""

from .models import Task


class TodoService:
    """Handles business logic for todo operations."""
    
    def __init__(self):
        """Initialize the TodoService with an empty task list."""
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title, description=""):
        """
        Add a new task to the list.
        
        Args:
            title (str): Required title of the task
            description (str): Optional description of the task
            
        Returns:
            Task: The newly created task
        """
        if not title:
            raise ValueError("Task title is required")
        
        task = Task(self.next_id, title, description, False)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_all_tasks(self):
        """
        Get all tasks in the list.
        
        Returns:
            list: List of all Task objects
        """
        return self.tasks
    
    def get_task_by_id(self, task_id):
        """
        Get a task by its ID.
        
        Args:
            task_id (int): The ID of the task to retrieve
            
        Returns:
            Task: The task with the specified ID, or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id, title=None, description=None):
        """
        Update an existing task.
        
        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            
        Returns:
            Task: The updated task, or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        
        if title is not None:
            if not title:
                raise ValueError("Task title cannot be empty")
            task.title = title
        
        if description is not None:
            task.description = description
        
        return task
    
    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): The ID of the task to delete
            
        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        return True
    
    def toggle_task_status(self, task_id):
        """
        Toggle the completion status of a task.
        
        Args:
            task_id (int): The ID of the task to toggle
            
        Returns:
            Task: The updated task, or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        
        task.completed = not task.completed
        return task