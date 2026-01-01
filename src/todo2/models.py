"""
Todo Console Application - Intermediate Level
Task data model with priority and tags
"""

from enum import Enum
from typing import Set, Optional
from datetime import datetime


class Priority(Enum):
    """Priority levels for tasks."""
    HIGH = "high"
    MEDIUM = "medium"  # Default
    LOW = "low"


class Task:
    """Represents a single todo task with enhanced features."""

    def __init__(self, task_id, title, description="", completed=False, 
                 priority=Priority.MEDIUM, tags: Optional[Set[str]] = None, 
                 due_date: Optional[datetime] = None):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str): Optional description of the task
            completed (bool): Completion status of the task (default: False)
            priority (Priority): Priority level of the task (default: MEDIUM)
            tags (Set[str]): Set of tags associated with the task (default: empty set)
            due_date (datetime): Optional due date for the task (default: None)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority if priority else Priority.MEDIUM
        self.tags = tags if tags else set()
        self.due_date = due_date

    def __str__(self):
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title} (Priority: {self.priority.value})"

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "tags": list(self.tags),
            "due_date": self.due_date.isoformat() if self.due_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary."""
        # Parse priority
        priority_value = data.get("priority", "medium")
        priority = Priority(priority_value) if priority_value in [p.value for p in Priority] else Priority.MEDIUM
        
        # Parse tags
        tags = set(data.get("tags", []))
        
        # Parse due date
        due_date = None
        if data.get("due_date"):
            try:
                from datetime import datetime as dt
                due_date = dt.fromisoformat(data["due_date"])
            except ValueError:
                due_date = None
        
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            priority=priority,
            tags=tags,
            due_date=due_date
        )