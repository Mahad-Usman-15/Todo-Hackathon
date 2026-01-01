"""
Todo Console Application - Advanced Level
Task data model with recurring, due dates, and reminders
"""

from enum import Enum
from typing import Set, Optional
from datetime import datetime


class Priority(Enum):
    """Priority levels for tasks."""
    HIGH = "high"
    MEDIUM = "medium"  # Default
    LOW = "low"


class RecurrencePattern(Enum):
    """Recurrence patterns for tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Task:
    """Represents a single todo task with advanced features."""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False,
                 priority=None, tags: Optional[Set[str]] = None,
                 due_date: Optional[datetime] = None, is_recurring: bool = False,
                 recurrence_pattern: Optional[RecurrencePattern] = None,
                 next_occurrence_date: Optional[datetime] = None,
                 has_reminder: bool = False, reminder_set: bool = False):
        """
        Initialize a Task instance with advanced features.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str): Optional description of the task
            completed (bool): Completion status of the task (default: False)
            priority: Priority level of the task (default: MEDIUM from imported Priority)
            tags (Set[str]): Set of tags associated with the task (default: empty set)
            due_date (datetime): Optional due date and time for the task (default: None)
            is_recurring (bool): Whether the task repeats (default: False)
            recurrence_pattern (RecurrencePattern): Pattern for recurrence if recurring (default: None)
            next_occurrence_date (datetime): When the next occurrence is due (default: None)
            has_reminder (bool): Whether to show notification (default: False)
            reminder_set (bool): Whether user has granted notification permission (default: False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority if priority else Priority.MEDIUM
        self.tags = tags if tags else set()
        self.due_date = due_date
        self.is_recurring = is_recurring
        self.recurrence_pattern = recurrence_pattern
        self.next_occurrence_date = next_occurrence_date
        self.has_reminder = has_reminder
        self.reminder_set = reminder_set

    def __str__(self):
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        recurring_info = f" (Recurring: {self.recurrence_pattern.value})" if self.is_recurring else ""
        due_info = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}: {self.title} (Priority: {self.priority.value}){recurring_info}{due_info}"

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "tags": list(self.tags),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern.value if self.recurrence_pattern else None,
            "next_occurrence_date": self.next_occurrence_date.isoformat() if self.next_occurrence_date else None,
            "has_reminder": self.has_reminder,
            "reminder_set": self.reminder_set
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

        # Parse next occurrence date
        next_occurrence_date = None
        if data.get("next_occurrence_date"):
            try:
                from datetime import datetime as dt
                next_occurrence_date = dt.fromisoformat(data["next_occurrence_date"])
            except ValueError:
                next_occurrence_date = None

        # Parse recurrence pattern
        recurrence_pattern = None
        if data.get("recurrence_pattern"):
            try:
                recurrence_pattern = RecurrencePattern(data["recurrence_pattern"])
            except ValueError:
                recurrence_pattern = None

        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            priority=priority,
            tags=tags,
            due_date=due_date,
            is_recurring=data.get("is_recurring", False),
            recurrence_pattern=recurrence_pattern,
            next_occurrence_date=next_occurrence_date,
            has_reminder=data.get("has_reminder", False),
            reminder_set=data.get("reminder_set", False)
        )