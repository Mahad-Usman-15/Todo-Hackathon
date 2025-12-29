"""
Todo Console Application
Task data model
"""

class Task:
    """Represents a single todo task."""
    
    def __init__(self, task_id, title, description="", completed=False):
        """
        Initialize a Task instance.
        
        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str): Optional description of the task
            completed (bool): Completion status of the task (default: False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title}"

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )