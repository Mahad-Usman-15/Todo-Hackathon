# Quickstart Guide: Advanced Level Tasks (Recurring & Reminders)

**Date**: 2026-01-01
**Feature**: 3-advanced-tasks

## Overview

This guide provides a quick introduction to implementing the Advanced Level features of the task management application, including recurring tasks, due dates with time, and time-based reminders.

## Prerequisites

- Python 3.13+ installed
- Basic understanding of the existing Basic and Intermediate Level task management systems
- Completed implementation of Basic and Intermediate Level features

## Implementation Steps

### 1. Update Task Model

First, enhance the existing Task model to include recurring, due date, and reminder functionality:

```python
from enum import Enum
from typing import Set, Optional
from datetime import datetime

class RecurrencePattern(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task:
    def __init__(self, id: int, title: str, description: str = "", 
                 completed: bool = False, priority: Priority = Priority.MEDIUM,
                 tags: Set[str] = None, due_date: Optional[datetime] = None,
                 is_recurring: bool = False, recurrence_pattern: Optional[RecurrencePattern] = None,
                 next_occurrence_date: Optional[datetime] = None,
                 has_reminder: bool = False, reminder_set: bool = False):
        self.id = id
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
```

### 2. Implement Recurring Task Logic

Add methods to handle recurring tasks:

```python
def complete_recurring_task(self, task_id: int):
    """Complete a recurring task and generate the next occurrence."""
    task = self.get_task(task_id)
    if not task or not task.is_recurring or not task.recurrence_pattern:
        return None
    
    # Mark current task as completed
    task.completed = True
    
    # Calculate next occurrence date based on recurrence pattern
    next_date = self.calculate_next_occurrence(task.due_date, task.recurrence_pattern)
    
    # Create a new task with the same properties but for the next occurrence
    new_task = Task(
        id=self.next_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        tags=task.tags,
        due_date=next_date,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        has_reminder=task.has_reminder
    )
    
    self.tasks.append(new_task)
    self.next_id += 1
    
    return new_task

def calculate_next_occurrence(self, current_date: datetime, pattern: RecurrencePattern):
    """Calculate the next occurrence date based on the recurrence pattern."""
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
```

### 3. Implement Due Date Handling

Add methods to handle due dates with time:

```python
def set_task_due_date(self, task_id: int, due_date: datetime):
    """Set a due date and time for a task."""
    task = self.get_task(task_id)
    if task:
        task.due_date = due_date
        return task
    return None

def get_overdue_tasks(self):
    """Get all tasks that are past their due date and not completed."""
    now = datetime.now()
    return [
        task for task in self.tasks
        if task.due_date and task.due_date < now and not task.completed
    ]

def get_tasks_due_soon(self, hours: int = 24):
    """Get all tasks due within the specified number of hours."""
    from datetime import timedelta
    now = datetime.now()
    future_time = now + timedelta(hours=hours)
    
    return [
        task for task in self.tasks
        if task.due_date and now < task.due_date <= future_time and not task.completed
    ]
```

### 4. Implement Reminder Functionality

Add methods to handle time-based reminders:

```python
import threading
import time

def enable_task_reminder(self, task_id: int):
    """Enable reminders for a task with a due date."""
    task = self.get_task(task_id)
    if task and task.due_date:
        task.has_reminder = True
        # Start a background thread to check for due reminders
        reminder_thread = threading.Thread(target=self.check_reminders, args=(task_id,), daemon=True)
        reminder_thread.start()
        return task
    return None

def check_reminders(self, task_id: int):
    """Check if a task's due time has arrived and trigger notification."""
    task = self.get_task(task_id)
    if not task or not task.has_reminder or not task.due_date:
        return
    
    while not task.completed:
        now = datetime.now()
        if task.due_date <= now:
            self.trigger_notification(task)
            break
        time.sleep(60)  # Check every minute

def trigger_notification(self, task):
    """Trigger a notification for a task."""
    # In a console application, this might just print a message
    # In a web application, this would use the browser's Notification API
    print(f"REMINDER: Task '{task.title}' is due now!")
```

### 5. Update CLI Interface

Add new commands to the CLI for the new features:

```python
def handle_set_recurring(self, args):
    """Handle setting a task as recurring."""
    if len(args) < 2:
        print("Usage: set-recurring <task_id> <pattern>")
        print("Patterns: daily, weekly, monthly")
        return
    
    try:
        task_id = int(args[0])
        pattern_str = args[1].lower()
        
        if pattern_str not in ['daily', 'weekly', 'monthly']:
            print("Invalid pattern. Use: daily, weekly, monthly")
            return
        
        pattern_map = {
            'daily': RecurrencePattern.DAILY,
            'weekly': RecurrencePattern.WEEKLY,
            'monthly': RecurrencePattern.MONTHLY
        }
        
        task = self.todo_service.set_task_recurring(task_id, pattern_map[pattern_str])
        if task:
            print(f"Task {task_id} set to recurring ({pattern_str} pattern)")
        else:
            print(f"Task {task_id} not found")
    except ValueError:
        print("Task ID must be a number")

def handle_set_due_date(self, args):
    """Handle setting a due date for a task."""
    if len(args) < 3:
        print("Usage: set-due-date <task_id> <YYYY-MM-DD> <HH:MM>")
        return
    
    try:
        task_id = int(args[0])
        date_str = args[1]  # Format: YYYY-MM-DD
        time_str = args[2]  # Format: HH:MM
        
        from datetime import datetime
        due_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        task = self.todo_service.set_task_due_date(task_id, due_datetime)
        if task:
            print(f"Due date set for task {task_id}: {due_datetime}")
        else:
            print(f"Task {task_id} not found")
    except ValueError:
        print("Invalid date/time format. Use: YYYY-MM-DD HH:MM")

def handle_set_reminder(self, args):
    """Handle enabling a reminder for a task."""
    if len(args) < 1:
        print("Usage: set-reminder <task_id>")
        return
    
    try:
        task_id = int(args[0])
        task = self.todo_service.enable_task_reminder(task_id)
        if task:
            print(f"Reminder enabled for task {task_id}")
        else:
            print(f"Task {task_id} not found or has no due date")
    except ValueError:
        print("Task ID must be a number")
```

## Testing

Ensure all new functionality is properly tested:

1. Unit tests for each new method
2. Integration tests for combined operations
3. Edge case tests (recurring tasks, due dates in the past, etc.)

## Verification

After implementation, verify:

1. All Basic and Intermediate Level functionality still works unchanged
2. New recurring task features work as expected
3. New due date features work as expected
4. New reminder features work as expected
5. Performance remains acceptable with additional features