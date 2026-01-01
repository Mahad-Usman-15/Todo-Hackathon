# Data Model: Intermediate Level Tasks (Organization & Usability)

**Date**: 2026-01-01
**Feature**: 1-intermediate-tasks
**Input**: Feature specification from `/specs/1-intermediate-tasks/spec.md`

## Overview

This document defines the data model for the Intermediate Level features of the task management application, including the enhanced Task entity with priority, tags, and related functionality.

## Entity: Task

### Fields
- **id**: int (auto-generated unique identifier)
- **title**: str (required, non-empty string)
- **description**: str (optional, can be empty)
- **completed**: bool (default: false)
- **priority**: Priority (enum: HIGH, MEDIUM, LOW; default: MEDIUM)
- **tags**: Set[str] (set of user-defined tags, default: empty set)
- **due_date**: Optional[datetime] (optional due date, default: None)

### Relationships
- A Task can have multiple Tags (many-to-many relationship through the tags field)
- A Tag can be associated with multiple Tasks (many-to-many relationship through the tags field)

### Validation Rules
- title must not be empty or None
- priority must be one of the defined Priority enum values
- tags must be a set of non-empty strings
- due_date must be a valid datetime object or None

### State Transitions
- A Task can transition from completed=False to completed=True (mark as complete)
- A Task can transition from completed=True to completed=False (mark as incomplete)
- Any field can be updated while maintaining the task's identity

## Entity: Priority (Enum)

### Values
- **HIGH**: Represents high priority tasks
- **MEDIUM**: Represents medium priority tasks (default)
- **LOW**: Represents low priority tasks

## Entity: Tag

### Fields
- **name**: str (required, unique identifier for the tag)

### Relationships
- A Tag can be associated with multiple Tasks (many-to-many relationship)
- Tags exist implicitly when assigned to tasks; no separate storage needed

### Validation Rules
- name must be a non-empty string
- name should not contain leading/trailing whitespace

## Entity: FilterCriteria

### Fields
- **status**: Optional[bool] (filter by completion status, default: None)
- **priority**: Optional[Priority] (filter by priority level, default: None)
- **tags**: Set[str] (filter by tags, default: empty set)
- **search_term**: Optional[str] (keyword search term, default: None)

### Validation Rules
- If tags set is not empty, only tasks containing at least one of the specified tags should be included
- search_term should be treated as case-insensitive substring match

## Entity: SortCriteria

### Fields
- **sort_by**: str (field to sort by: 'due_date', 'priority', 'title', 'status')
- **ascending**: bool (sort direction, default: true)

### Validation Rules
- sort_by must be one of the allowed values
- ascending must be a boolean value