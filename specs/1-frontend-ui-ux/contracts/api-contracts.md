# API Contracts: Frontend Web Application

## Authentication API Contracts

### Login Endpoint
```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (200):
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "User Name"
  },
  "token": "jwt-token-string"
}

Response (401):
{
  "error": "Invalid credentials"
}
```

## Task Management API Contracts

### Get User Tasks
```
GET /api/{user_id}/tasks
Authorization: Bearer {jwt_token}

Response (200):
{
  "data": [
    {
      "id": "task-uuid",
      "title": "Task Title",
      "description": "Task description",
      "completed": false,
      "createdAt": "2026-01-06T10:00:00Z",
      "updatedAt": "2026-01-06T10:00:00Z",
      "userId": "user-uuid"
    }
  ]
}

Response (401):
{
  "error": "Unauthorized"
}
```

### Create Task
```
POST /api/{user_id}/tasks
Authorization: Bearer {jwt_token}
Content-Type: application/json

Request:
{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}

Response (201):
{
  "data": {
    "id": "new-task-uuid",
    "title": "New Task",
    "description": "Task description",
    "completed": false,
    "createdAt": "2026-01-06T10:00:00Z",
    "updatedAt": "2026-01-06T10:00:00Z",
    "userId": "user-uuid"
  }
}

Response (401):
{
  "error": "Unauthorized"
}

Response (422):
{
  "error": "Validation failed",
  "details": {
    "title": "Title is required and must be 1-100 characters"
  }
}
```

### Update Task
```
PUT /api/{user_id}/tasks/{id}
Authorization: Bearer {jwt_token}
Content-Type: application/json

Request:
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}

Response (200):
{
  "data": {
    "id": "task-uuid",
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true,
    "createdAt": "2026-01-06T10:00:00Z",
    "updatedAt": "2026-01-06T11:00:00Z",
    "userId": "user-uuid"
  }
}

Response (401):
{
  "error": "Unauthorized"
}

Response (404):
{
  "error": "Task not found"
}
```

### Delete Task
```
DELETE /api/{user_id}/tasks/{id}
Authorization: Bearer {jwt_token}

Response (204): No content

Response (401):
{
  "error": "Unauthorized"
}

Response (404):
{
  "error": "Task not found"
}
```

### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
Authorization: Bearer {jwt_token}
Content-Type: application/json

Request:
{
  "completed": true
}

Response (200):
{
  "data": {
    "id": "task-uuid",
    "title": "Task Title",
    "description": "Task description",
    "completed": true,
    "createdAt": "2026-01-06T10:00:00Z",
    "updatedAt": "2026-01-06T11:00:00Z",
    "userId": "user-uuid"
  }
}

Response (401):
{
  "error": "Unauthorized"
}

Response (404):
{
  "error": "Task not found"
}
```