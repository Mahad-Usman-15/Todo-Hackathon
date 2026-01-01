# Quickstart Guide: Intermediate Level Tasks (Organization & Usability)

**Date**: 2026-01-01
**Feature**: 1-intermediate-tasks

## Overview

This guide provides a quick introduction to implementing the Intermediate Level features of the task management application, including task priorities, tags/categories, search functionality, filtering, and sorting.

## Prerequisites

- Python 3.13+ installed
- Basic understanding of the existing Basic Level task management system
- Completed implementation of Basic Level features

## Implementation Steps

### 1. Update Task Model

First, enhance the existing Task model to include priority and tags:

```python
from enum import Enum
from typing import Set, Optional
from datetime import datetime

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"  # Default
    LOW = "low"

class Task:
    def __init__(self, id: int, title: str, description: str = "", 
                 completed: bool = False, priority: Priority = Priority.MEDIUM,
                 tags: Set[str] = None, due_date: Optional[datetime] = None):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority if priority else Priority.MEDIUM
        self.tags = tags if tags else set()
        self.due_date = due_date
```

### 2. Implement Priority Handling

Add methods to handle task priorities:

```python
def update_task_priority(self, task_id: int, priority: Priority):
    """Update the priority of a specific task"""
    task = self.get_task(task_id)
    if task:
        task.priority = priority
        return task
    return None

def get_tasks_by_priority(self, priority: Priority):
    """Get all tasks with a specific priority"""
    return [task for task in self.tasks if task.priority == priority]
```

### 3. Implement Tag Handling

Add methods to handle task tags:

```python
def add_tag_to_task(self, task_id: int, tag: str):
    """Add a tag to a specific task"""
    task = self.get_task(task_id)
    if task and tag.strip():
        task.tags.add(tag.strip())
        return task
    return None

def remove_tag_from_task(self, task_id: int, tag: str):
    """Remove a tag from a specific task"""
    task = self.get_task(task_id)
    if task and tag in task.tags:
        task.tags.remove(tag)
        return task
    return None

def get_tasks_by_tag(self, tag: str):
    """Get all tasks with a specific tag"""
    return [task for task in self.tasks if tag in task.tags]
```

### 4. Implement Search Functionality

Add search capabilities:

```python
def search_tasks(self, search_term: str):
    """Search tasks by keyword in title and description"""
    if not search_term:
        return self.tasks
    
    search_lower = search_term.lower()
    return [
        task for task in self.tasks
        if search_lower in task.title.lower() or 
           search_lower in task.description.lower()
    ]
```

### 5. Implement Filtering

Add filtering capabilities:

```python
def filter_tasks(self, status: Optional[bool] = None, 
                 priority: Optional[Priority] = None,
                 tags: Set[str] = None):
    """Filter tasks by various criteria"""
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
```

### 6. Implement Sorting

Add sorting capabilities:

```python
from operator import attrgetter

def sort_tasks(self, sort_by: str, ascending: bool = True):
    """Sort tasks by specified criteria"""
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
```

### 7. Update CLI Interface

Add new commands to the CLI for the new features:

```python
def handle_set_priority(self, args):
    """Handle setting task priority"""
    if len(args) != 2:
        print("Usage: set-priority <task_id> <priority>")
        return
    
    try:
        task_id = int(args[0])
        priority_str = args[1].upper()
        if priority_str in ['HIGH', 'MEDIUM', 'LOW']:
            priority = Priority[priority_str]
            task = self.todo_service.update_task_priority(task_id, priority)
            if task:
                print(f"Priority set to {priority.value} for task {task_id}")
            else:
                print(f"Task {task_id} not found")
        else:
            print("Priority must be one of: HIGH, MEDIUM, LOW")
    except ValueError:
        print("Task ID must be a number")

def handle_add_tag(self, args):
    """Handle adding a tag to a task"""
    if len(args) != 2:
        print("Usage: add-tag <task_id> <tag>")
        return
    
    try:
        task_id = int(args[0])
        tag = args[1]
        task = self.todo_service.add_tag_to_task(task_id, tag)
        if task:
            print(f"Tag '{tag}' added to task {task_id}")
        else:
            print(f"Task {task_id} not found")
    except ValueError:
        print("Task ID must be a number")

def handle_search(self, args):
    """Handle searching tasks"""
    if not args:
        print("Usage: search <keyword>")
        return
    
    search_term = ' '.join(args)
    tasks = self.todo_service.search_tasks(search_term)
    
    if tasks:
        print(f"Found {len(tasks)} matching tasks:")
        self.display_tasks(tasks)
    else:
        print("No tasks found matching the search term")
```

## Testing

Ensure all new functionality is properly tested:

1. Unit tests for each new method
2. Integration tests for combined operations
3. Edge case tests (empty searches, invalid priorities, etc.)

## Verification

After implementation, verify:

1. All Basic Level functionality still works unchanged
2. New priority features work as expected
3. New tagging features work as expected
4. Search functionality works correctly
5. Filtering works with all criteria
6. Sorting works with all criteria
7. Performance remains acceptable with larger task lists