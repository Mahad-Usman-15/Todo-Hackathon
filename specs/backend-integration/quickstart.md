# Quickstart Guide: Backend Integration for Todo Full-Stack Web Application

## Prerequisites

- Python 3.11+
- pip package manager
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Better Auth configured for frontend (to obtain JWT tokens)

## Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install fastapi sqlmodel uvicorn python-multipart python-jose[cryptography] psycopg2-binary
   ```

## Configuration

Create a `.env` file in the backend directory with the following environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
BETTER_AUTH_SECRET=your_better_auth_secret_here
```

## Running the Application

1. **Start the development server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **The API will be available at:**
   - Base URL: `http://localhost:8000`
   - API endpoints: `http://localhost:8000/api/{user_id}/tasks`
   - Interactive docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## API Usage Examples

### Getting Authorization Token
First, authenticate with Better Auth to obtain a JWT token. This token must be included in the Authorization header for all API requests.

### 1. Create a Task
```bash
curl -X POST "http://localhost:8000/api/user-123/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task",
    "due_date": "2023-12-31T23:59:59Z"
  }'
```

### 2. Get All Tasks
```bash
curl -X GET "http://localhost:8000/api/user-123/tasks?status=all&sort=created" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 3. Update a Task
```bash
curl -X PUT "http://localhost:8000/api/user-123/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated description",
    "due_date": "2023-12-31T23:59:59Z"
  }'
```

### 4. Toggle Task Completion
```bash
curl -X PATCH "http://localhost:8000/api/user-123/tasks/1/complete" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 5. Delete a Task
```bash
curl -X DELETE "http://localhost:8000/api/user-123/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Database Setup

1. **Initialize the database:**
   ```bash
   # Run the application to create tables automatically
   uvicorn main:app --reload
   ```

   Or manually run initialization if your main.py includes a startup event.

2. **For Neon Serverless PostgreSQL:**
   - Create a project at https://neon.tech
   - Get your connection string
   - Update the DATABASE_URL in your .env file

## Testing

Run the tests using pytest:
```bash
pip install pytest pytest-asyncio httpx
pytest tests/
```

## Project Structure
```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel database models
├── db.py                # Database connection and session management
├── auth.py              # JWT authentication utilities
├── routes/
│   ├── __init__.py
│   ├── tasks.py         # Task-related API endpoints
│   └── auth.py          # Authentication-related endpoints
├── schemas/             # Pydantic request/response models
│   ├── __init__.py
│   ├── task.py
│   └── user.py
├── config.py            # Configuration and environment variables
├── dependencies.py      # FastAPI dependency injection functions
├── utils/
│   ├── __init__.py
│   └── validators.py    # Validation utilities
├── middleware/
│   ├── __init__.py
│   └── auth_middleware.py  # JWT authentication middleware
└── tests/
    ├── conftest.py
    ├── test_tasks.py    # Task API tests
    ├── test_auth.py     # Authentication tests
    └── integration/
        └── test_task_integration.py
```

## Troubleshooting

- **Database connection issues**: Verify your DATABASE_URL is correct and the database server is running
- **Authentication errors**: Ensure your JWT token is valid and the BETTER_AUTH_SECRET matches the one used to generate the token
- **403 Forbidden errors**: Verify that you're only accessing tasks that belong to your user_id
- **Validation errors**: Check that your request body conforms to the required schema (e.g., title between 1-200 chars)