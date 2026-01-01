"""
Todo Console Application - Advanced Level
Business logic layer with recurring, due dates, and reminders
"""

from models import Task, RecurrencePattern, Priority
from typing import Set, Optional
from datetime import datetime
import threading
import time


class TodoService:
    """Handles business logic for todo operations with advanced features."""

    def __init__(self):
        """Initialize the TodoService with an empty task list."""
        self.tasks = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM, 
                 tags: Optional[Set[str]] = None, due_date: Optional[datetime] = None,
                 is_recurring: bool = False, recurrence_pattern: Optional[RecurrencePattern] = None,
                 has_reminder: bool = False):
        """
        Add a new task to the list with advanced features.

        Args:
            title (str): Required title of the task
            description (str): Optional description of the task
            priority (Priority): Priority level of the task (default: MEDIUM)
            tags (Set[str]): Set of tags associated with the task (default: empty set)
            due_date (datetime): Optional due date for the task (default: None)
            is_recurring (bool): Whether the task repeats (default: False)
            recurrence_pattern (RecurrencePattern): Pattern for recurrence if recurring (default: None)
            has_reminder (bool): Whether to show notification (default: False)

        Returns:
            Task: The newly created task
        """
        if not title:
            raise ValueError("Task title is required")

        task = Task(
            self.next_id, title, description, False, priority, tags, 
            due_date, is_recurring, recurrence_pattern, None, has_reminder
        )
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

        # If the task is recurring and is being completed, create a new occurrence
        if task.is_recurring and not task.completed:
            new_task = self.complete_recurring_task(task_id)
            return new_task or task  # Return the new task if created, otherwise the original
        else:
            task.completed = not task.completed
            return task

    def complete_recurring_task(self, task_id: int):
        """
        Complete a recurring task and generate the next occurrence.

        Args:
            task_id (int): The ID of the recurring task to complete

        Returns:
            Task: The new occurrence of the task, or None if not recurring
        """
        task = self.get_task_by_id(task_id)
        if not task or not task.is_recurring or not task.recurrence_pattern:
            return None

        # Mark current task as completed
        task.completed = True

        # Calculate next occurrence date based on recurrence pattern
        next_date = self.calculate_next_occurrence(task.due_date, task.recurrence_pattern)

        # Create a new task with the same properties but for the next occurrence
        new_task = Task(
            self.next_id, 
            task.title,
            task.description,
            False,  # New task is not completed
            task.priority,
            task.tags.copy(),  # Copy the tags
            next_date,  # New due date
            task.is_recurring,
            task.recurrence_pattern,
            None,  # No next occurrence date yet
            task.has_reminder  # Keep the reminder setting
        )

        self.tasks.append(new_task)
        self.next_id += 1

        return new_task

    def calculate_next_occurrence(self, current_date: datetime, pattern: RecurrencePattern):
        """
        Calculate the next occurrence date based on the recurrence pattern.

        Args:
            current_date (datetime): The current date to calculate from
            pattern (RecurrencePattern): The recurrence pattern

        Returns:
            datetime: The next occurrence date
        """
        if current_date is None:
            # If no current date, use today
            current_date = datetime.now()
        
        if pattern == RecurrencePattern.DAILY:
            return current_date.replace(day=current_date.day + 1)
        elif pattern == RecurrencePattern.WEEKLY:
            return current_date.replace(day=current_date.day + 7)
        elif pattern == RecurrencePattern.MONTHLY:
            # Handle month overflow (e.g., Jan 31 -> Feb 28/29)
            next_month = current_date.month + 1
            next_year = current_date.year
            if next_month > 12:
                next_month = 1
                next_year += 1

            # Handle case where the day doesn't exist in the next month (e.g., Jan 31 -> Feb 31 doesn't exist)
            import calendar
            max_day = calendar.monthrange(next_year, next_month)[1]
            next_day = min(current_date.day, max_day)

            return current_date.replace(year=next_year, month=next_month, day=next_day)

        return current_date

    def set_task_due_date(self, task_id: int, due_date: datetime):
        """
        Set a due date and time for a task.

        Args:
            task_id (int): The ID of the task
            due_date (datetime): The due date to set

        Returns:
            Task: The updated task, or None if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.due_date = due_date
            return task
        return None

    def get_overdue_tasks(self):
        """
        Get all tasks that are past their due date and not completed.

        Returns:
            list: List of overdue tasks
        """
        now = datetime.now()
        return [
            task for task in self.tasks
            if task.due_date and task.due_date < now and not task.completed
        ]

    def get_tasks_due_soon(self, hours: int = 24):
        """
        Get all tasks due within the specified number of hours.

        Args:
            hours (int): Number of hours ahead to check (default: 24)

        Returns:
            list: List of tasks due soon
        """
        from datetime import timedelta
        now = datetime.now()
        future_time = now + timedelta(hours=hours)

        return [
            task for task in self.tasks
            if task.due_date and now < task.due_date <= future_time and not task.completed
        ]

    def enable_task_reminder(self, task_id: int):
        """
        Enable reminders for a task with a due date.

        Args:
            task_id (int): The ID of the task

        Returns:
            Task: The updated task, or None if not found or invalid
        """
        task = self.get_task_by_id(task_id)
        if task and task.due_date:
            task.has_reminder = True
            # Start a background thread to check for due reminders
            reminder_thread = threading.Thread(target=self.check_reminders, args=(task_id,), daemon=True)
            reminder_thread.start()
            return task
        return None

    def check_reminders(self, task_id: int):
        """
        Check if a task's due time has arrived and trigger notification.

        Args:
            task_id (int): The ID of the task to check
        """
        task = self.get_task_by_id(task_id)
        if not task or not task.has_reminder or not task.due_date:
            return

        while not task.completed:
            now = datetime.now()
            if task.due_date <= now:
                self.trigger_notification(task)
                break
            time.sleep(60)  # Check every minute

    def trigger_notification(self, task):
        """
        Trigger a notification for a task.

        Args:
            task (Task): The task to notify about
        """
        # In a console application, this might just print a message
        print(f"REMINDER: Task '{task.title}' is due now!")