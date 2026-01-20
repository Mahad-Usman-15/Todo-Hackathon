# Todo Backend API

This is the backend service for the Todo application, built with FastAPI and SQLModel. Provides secure task management with user isolation and authentication.

## Features

- Secure task management with JWT-based authentication
- User isolation to ensure data privacy
- RESTful API endpoints for task CRUD operations
- Rate limiting to prevent abuse
- Comprehensive logging for monitoring
- Concurrent request handling with proper locking
- Input sanitization to prevent injection attacks
- Persistent storage with Neon Serverless PostgreSQL

## API Endpoints

### Task Management

- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Retrieve user's tasks with optional filtering
- `PUT /api/{user_id}/tasks/{id}` - Update an existing task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

### System

- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint for monitoring

## API Usage Examples

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Create a Task
```
POST /api/user123/tasks
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "title": "Sample Task",
  "description": "Task description",
  "due_date": "2023-12-31T10:00:00Z"
}
```

### Get User's Tasks
```
GET /api/user123/tasks?status=all&sort=created&limit=10&offset=0
Authorization: Bearer <jwt-token>
```

Query Parameters:
- `status`: all, pending, or completed (default: all)
- `sort`: created, title, or due_date (default: created)
- `limit`: number of tasks to return (max: 100)
- `offset`: number of tasks to skip

### Update a Task
```
PUT /api/user123/tasks/1
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

### Toggle Task Completion
```
PATCH /api/user123/tasks/1/complete
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "completed": true
}
```

### Delete a Task
```
DELETE /api/user123/tasks/1
Authorization: Bearer <jwt-token>
```

## Rate Limits
- Task creation: 10 per minute per IP
- Task retrieval: 50 per minute per IP
- Task updates: 20 per minute per IP
- Task deletion: 15 per minute per IP
- Completion updates: 30 per minute per IP

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and auth secret
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for JWT token validation

## Testing

Run the tests:
```bash
pytest
```

## API Documentation

Interactive API documentation is available at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation
- `/openapi.json` - OpenAPI specification

## License

MIT