"""
Todo Console Application - Intermediate Level
Business logic layer with priority and tagging features
"""

from models import Task, Priority
from typing import Set, Optional
from datetime import datetime


class TodoService:
    """Handles business logic for todo operations with enhanced features."""

    def __init__(self):
        """Initialize the TodoService with an empty task list."""
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, description="", priority=Priority.MEDIUM, tags: Optional[Set[str]] = None, due_date: Optional[datetime] = None):
        """
        Add a new task to the list.

        Args:
            title (str): Required title of the task
            description (str): Optional description of the task
            priority (Priority): Priority level of the task (default: MEDIUM)
            tags (Set[str]): Set of tags associated with the task (default: empty set)
            due_date (datetime): Optional due date for the task (default: None)

        Returns:
            Task: The newly created task
        """
        if not title:
            raise ValueError("Task title is required")

        task = Task(self.next_id, title, description, False, priority, tags, due_date)
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

    def update_task_priority(self, task_id: int, priority: Priority):
        """
        Update the priority of a specific task.

        Args:
            task_id (int): The ID of the task to update
            priority (Priority): The new priority level

        Returns:
            Task: The updated task, or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.priority = priority
            return task
        return None

    def get_tasks_by_priority(self, priority: Priority):
        """
        Get all tasks with a specific priority.

        Args:
            priority (Priority): The priority level to filter by

        Returns:
            list: List of tasks with the specified priority
        """
        return [task for task in self.tasks if task.priority == priority]

    def add_tag_to_task(self, task_id: int, tag: str):
        """
        Add a tag to a specific task.

        Args:
            task_id (int): The ID of the task to update
            tag (str): The tag to add

        Returns:
            Task: The updated task, or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if task and tag.strip():
            task.tags.add(tag.strip())
            return task
        return None

    def remove_tag_from_task(self, task_id: int, tag: str):
        """
        Remove a tag from a specific task.

        Args:
            task_id (int): The ID of the task to update
            tag (str): The tag to remove

        Returns:
            Task: The updated task, or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if task and tag in task.tags:
            task.tags.remove(tag)
            return task
        return None

    def get_tasks_by_tag(self, tag: str):
        """
        Get all tasks with a specific tag.

        Args:
            tag (str): The tag to filter by

        Returns:
            list: List of tasks with the specified tag
        """
        return [task for task in self.tasks if tag in task.tags]

    def search_tasks(self, search_term: str):
        """
        Search tasks by keyword in title and description.

        Args:
            search_term (str): The keyword to search for

        Returns:
            list: List of tasks matching the search term
        """
        if not search_term:
            return self.tasks

        search_lower = search_term.lower()
        return [
            task for task in self.tasks
            if search_lower in task.title.lower() or
               search_lower in task.description.lower()
        ]

    def filter_tasks(self, status: Optional[bool] = None,
                     priority: Optional[Priority] = None,
                     tags: Optional[Set[str]] = None):
        """
        Filter tasks by various criteria.

        Args:
            status (bool, optional): Filter by completion status
            priority (Priority, optional): Filter by priority level
            tags (Set[str], optional): Filter by tags

        Returns:
            list: List of tasks matching the filter criteria
        """
        filtered_tasks = self.tasks

        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == status]

        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        if tags:
            filtered_tasks = [
                task for task in filtered_tasks
                if any(tag in task.tags for tag in tags)
            ]

        return filtered_tasks

    def sort_tasks(self, sort_by: str, ascending: bool = True):
        """
        Sort tasks by specified criteria.

        Args:
            sort_by (str): Field to sort by ('priority', 'title', 'id', 'due_date')
            ascending (bool): Sort direction (default: True)

        Returns:
            list: List of tasks sorted by the specified criteria
        """
        from operator import attrgetter

        if sort_by == 'priority':
            # Define priority order for sorting
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            sorted_tasks = sorted(
                self.tasks,
                key=lambda task: priority_order[task.priority],
                reverse=not ascending
            )
        elif sort_by == 'due_date':
            sorted_tasks = sorted(
                self.tasks,
                key=lambda task: (task.due_date is None, task.due_date),
                reverse=not ascending
            )
        elif sort_by == 'title':
            sorted_tasks = sorted(
                self.tasks,
                key=attrgetter('title'),
                reverse=not ascending
            )
        else:  # Default to sorting by ID
            sorted_tasks = sorted(
                self.tasks,
                key=attrgetter('id'),
                reverse=not ascending
            )

        return sorted_tasks