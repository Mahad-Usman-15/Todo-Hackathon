# API Contracts: Intermediate Level Tasks (Organization & Usability)

**Date**: 2026-01-01
**Feature**: 1-intermediate-tasks

## Overview

This document defines the API contracts for the Intermediate Level features of the task management application.

## Task Priority Operations

### Set Task Priority
- **Command**: `set-priority <task_id> <priority>`
- **Parameters**:
  - `task_id`: integer ID of the task
  - `priority`: string value (HIGH, MEDIUM, LOW)
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, invalid priority value

### Get Tasks by Priority
- **Command**: `filter --priority <priority>`
- **Parameters**:
  - `priority`: string value (HIGH, MEDIUM, LOW)
- **Response**: List of tasks with specified priority
- **Error Cases**: Invalid priority value

## Task Tag Operations

### Add Tag to Task
- **Command**: `add-tag <task_id> <tag>`
- **Parameters**:
  - `task_id`: integer ID of the task
  - `tag`: string tag name
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, invalid tag format

### Remove Tag from Task
- **Command**: `remove-tag <task_id> <tag>`
- **Parameters**:
  - `task_id`: integer ID of the task
  - `tag`: string tag name
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, task doesn't have the tag

### Get Tasks by Tag
- **Command**: `filter --tag <tag>`
- **Parameters**:
  - `tag`: string tag name
- **Response**: List of tasks with specified tag
- **Error Cases**: No tasks found with the tag

## Search Operations

### Search Tasks
- **Command**: `search <keyword>`
- **Parameters**:
  - `keyword`: string to search for in titles and descriptions
- **Response**: List of tasks matching the keyword
- **Error Cases**: No tasks found matching the keyword

## Filter Operations

### Filter Tasks
- **Command**: `filter [options]`
- **Options**:
  - `--status <completed|pending>`: Filter by completion status
  - `--priority <HIGH|MEDIUM|LOW>`: Filter by priority
  - `--tag <tag>`: Filter by tag
- **Response**: List of tasks matching all filter criteria
- **Error Cases**: Invalid filter options, no tasks match criteria

## Sort Operations

### Sort Tasks
- **Command**: `sort --by <field> [--order <asc|desc>]`
- **Options**:
  - `--by <due_date|priority|title>`: Field to sort by
  - `--order <asc|desc>`: Sort order (default: asc)
- **Response**: List of tasks sorted by specified criteria
- **Error Cases**: Invalid sort field or order