# API Contracts: Advanced Level Tasks (Recurring & Reminders)

**Date**: 2026-01-01
**Feature**: 3-advanced-tasks

## Overview

This document defines the API contracts for the Advanced Level features of the task management application.

## Recurring Task Operations

### Set Task as Recurring
- **Command**: `set-recurring <task_id> <pattern>`
- **Parameters**:
  - `task_id`: integer ID of the task
  - `pattern`: string value (daily, weekly, monthly)
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, invalid pattern value

### Complete Recurring Task
- **Command**: `complete <task_id>` (existing command with enhanced functionality)
- **Parameters**:
  - `task_id`: integer ID of the task
- **Response**: Success message and new occurrence ID if recurring
- **Error Cases**: Task ID doesn't exist

## Due Date Operations

### Set Task Due Date
- **Command**: `set-due-date <task_id> <date> <time>`
- **Parameters**:
  - `task_id`: integer ID of the task
  - `date`: date in YYYY-MM-DD format
  - `time`: time in HH:MM format
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, invalid date/time format

### Get Overdue Tasks
- **Command**: `filter --overdue`
- **Parameters**: None
- **Response**: List of tasks past their due date and not completed
- **Error Cases**: No overdue tasks found

### Get Tasks Due Soon
- **Command**: `filter --due-soon [hours]`
- **Parameters**:
  - `hours`: optional number of hours ahead to check (default: 24)
- **Response**: List of tasks due within the specified time
- **Error Cases**: No tasks due soon

## Reminder Operations

### Enable Task Reminder
- **Command**: `set-reminder <task_id>`
- **Parameters**:
  - `task_id`: integer ID of the task
- **Response**: Success message or error if task not found
- **Error Cases**: Task ID doesn't exist, task has no due date

### Check Reminders
- **Command**: Internal operation that runs continuously
- **Parameters**: None
- **Response**: Browser notifications when due time arrives
- **Error Cases**: Notification permission denied