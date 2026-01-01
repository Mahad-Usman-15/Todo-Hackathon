# Data Model: Advanced Level Tasks (Recurring & Reminders)

**Date**: 2026-01-01
**Feature**: 3-advanced-tasks
**Input**: Feature specification from `/specs/3-advanced-tasks/spec.md`

## Overview

This document defines the data model for the Advanced Level features of the task management application, including the enhanced Task entity with recurring functionality, due dates, and reminder capabilities.

## Entity: Task

### Fields
- **id**: int (auto-generated unique identifier)
- **title**: str (required, non-empty string)
- **description**: str (optional, can be empty)
- **completed**: bool (default: false)
- **priority**: Priority (enum: HIGH, MEDIUM, LOW; default: MEDIUM)
- **tags**: Set[str] (set of user-defined tags, default: empty set)
- **due_date**: Optional[datetime] (optional due date and time, default: None)
- **is_recurring**: bool (whether the task repeats, default: false)
- **recurrence_pattern**: Optional[RecurrencePattern] (pattern for recurrence if recurring, default: None)
- **next_occurrence_date**: Optional[datetime] (when the next occurrence is due, default: None)
- **has_reminder**: bool (whether to show notification, default: false)
- **reminder_set**: bool (whether user has granted notification permission, default: false)

### Relationships
- A Task can have multiple Tags (many-to-many relationship through the tags field)
- A Tag can be associated with multiple Tasks (many-to-many relationship through the tags field)

### Validation Rules
- title must not be empty or None
- priority must be one of the defined Priority enum values
- tags must be a set of non-empty strings
- due_date must be a valid datetime object or None
- if is_recurring is True, recurrence_pattern must be specified
- if has_reminder is True, due_date must be specified

### State Transitions
- A Task can transition from completed=False to completed=True (mark as complete)
- A Task can transition from completed=True to completed=False (mark as incomplete)
- A recurring Task can generate a new occurrence after completion
- Any field can be updated while maintaining the task's identity

## Entity: RecurrencePattern (Enum)

### Values
- **DAILY**: Represents daily recurring tasks
- **WEEKLY**: Represents weekly recurring tasks
- **MONTHLY**: Represents monthly recurring tasks

## Entity: Reminder

### Fields
- **enabled**: bool (whether reminders are enabled for the task, default: false)
- **notification_permission**: bool (whether browser permission was granted, default: false)
- **content**: str (content to display in notification, default: task title)

### Relationships
- A Reminder is associated with one Task (one-to-one relationship)

### Validation Rules
- If enabled is True, notification_permission must be True
- Content must not be empty

## Entity: FilterCriteria

### Fields
- **status**: Optional[bool] (filter by completion status, default: None)
- **priority**: Optional[Priority] (filter by priority level, default: None)
- **tags**: Set[str] (filter by tags, default: empty set)
- **search_term**: Optional[str] (keyword search term, default: None)
- **has_due_date**: Optional[bool] (filter by presence of due date, default: None)
- **is_recurring**: Optional[bool] (filter by recurrence status, default: None)

### Validation Rules
- If tags set is not empty, only tasks containing at least one of the specified tags should be included
- search_term should be treated as case-insensitive substring match

## Entity: SortCriteria

### Fields
- **sort_by**: str (field to sort by: 'due_date', 'priority', 'title', 'status', 'recurrence')
- **ascending**: bool (sort direction, default: true)

### Validation Rules
- sort_by must be one of the allowed values
- ascending must be a boolean value