# Data Model: Backend Integration for Todo Full-Stack Web Application

## Overview
This document defines the data models for the Todo application backend, including entity relationships, field definitions, and validation rules based on the feature specification.

## Task Entity

### Fields
- **id** (Integer, Primary Key, Auto-generated)
  - Unique identifier for each task
  - Auto-incremented integer value
- **user_id** (String/UUID, Foreign Key, Required)
  - Identifies the owner of the task
  - Must match the authenticated user's ID for access
  - Used for enforcing user isolation
- **title** (String, Required, 1-200 characters)
  - The task title/description in brief
  - Must be between 1 and 200 characters inclusive
  - Cannot be empty or whitespace-only
- **description** (String, Optional, 0-1000 characters)
  - Detailed description of the task
  - Can be empty or null
  - Maximum length of 1000 characters
- **due_date** (DateTime, Optional)
  - Deadline for the task completion
  - Can be null if no deadline is set
  - Used for sorting and filtering operations
- **completed** (Boolean, Required, Default: False)
  - Status indicating if the task is completed
  - True if completed, False if pending
  - Default value is False for new tasks
- **created_at** (DateTime, Required, Auto-generated)
  - Timestamp when the task was created
  - Automatically set on creation
- **updated_at** (DateTime, Required, Auto-generated)
  - Timestamp when the task was last updated
  - Automatically updated on any modification

### Relationships
- **Task** belongs to **User** (via user_id foreign key)
  - Each task is owned by exactly one user
  - User can own multiple tasks

### Validation Rules
- Title must be between 1-200 characters
- Description must be between 0-1000 characters if provided
- user_id must match the authenticated user's ID for operations
- Completed status can only be modified by the task owner
- Creation and update timestamps are automatically managed

### Indexes
- Index on user_id (for efficient user-based queries)
- Index on completed (for efficient status-based filtering)
- Composite index on (user_id, completed) for combined filtering

## User Entity (Managed by Better Auth)

### Fields
- **id** (String/UUID, Primary Key)
  - Unique identifier for the user
  - Managed by Better Auth system
- **email** (String)
  - User's email address
  - Managed by Better Auth system
- **name** (String)
  - User's display name
  - Managed by Better Auth system

### Relationships
- **User** has many **Tasks** (via user_id foreign key in tasks table)

## State Transitions

### Task Completion
- **Pending** → **Completed**: When user marks task as complete
- **Completed** → **Pending**: When user unmarks task as complete

### Task Lifecycle
- **Created**: New task added to user's task list
- **Modified**: Task details updated by user
- **Deleted**: Task removed from user's task list (soft delete not implemented)

## Database Schema

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

Note: The users table is managed by Better Auth and is referenced by the tasks table via the user_id foreign key.