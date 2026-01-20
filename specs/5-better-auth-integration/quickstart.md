# Quickstart Guide: Better Auth (JWT) Integration

## Overview
This guide provides step-by-step instructions to implement Better Auth (JWT) integration into the existing Todo app.

## Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ with pip
- PostgreSQL database (Neon Serverless recommended)
- Environment variables configured:
  - `DATABASE_URL` - PostgreSQL connection string
  - `BETTER_AUTH_SECRET` - Secret for JWT signing (32+ random characters)

## Step 1: Install Dependencies

### Frontend (Next.js)
```bash
npm install better-auth @better-auth/client-react
# or
yarn add better-auth @better-auth/client-react
```

### Backend (FastAPI)
```bash
pip install python-jose[cryptography] python-multipart
```

## Step 2: Configure Better Auth in Frontend

Create `lib/auth.ts` in your Next.js project:

```typescript
import { BetterAuthClient } from "better-auth/client";
import { jwt } from "better-auth/plugins";

export const authClient = new BetterAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:4000",
  plugins: [
    jwt({
      secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET!,
    }),
  ],
});
```

Set up the auth provider in your root layout (`app/layout.tsx`):

```tsx
import { BetterAuthProvider } from "better-auth/react";
import { auth } from "../lib/better-auth"; // Your auth config

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <BetterAuthProvider value={auth}>
          {children}
        </BetterAuthProvider>
      </body>
    </html>
  );
}
```

## Step 3: Configure Better Auth Backend

Create the auth configuration in your backend:

```typescript
import { BetterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = BetterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
    }),
  ],
  // Additional configuration as needed
});
```

## Step 4: Implement JWT Validation Middleware in FastAPI

Create JWT validation utilities in your FastAPI backend:

```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
import os

# Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

def verify_token(token: str) -> TokenData:
    """
    Verify the JWT token and return user information
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, email=email)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    """
    Dependency to get current user from JWT token
    """
    token = credentials.credentials
    return verify_token(token)
```

## Step 5: Update API Routes with Authentication

Modify your existing task endpoints to include authentication:

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/api")

@router.get("/tasks", response_model=List[Task])
async def get_tasks(current_user: TokenData = Depends(get_current_user)):
    """
    Get all tasks for the current user
    """
    # Verify the user ID in the token matches the expected user
    # Query the database for tasks filtered by current_user.user_id
    # This implements database-level row security
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.user_id)
    ).all()
    return tasks

@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: TokenData = Depends(get_current_user)):
    """
    Create a task for the current user
    """
    # Ensure the task is created for the current user
    # by setting task.user_id = current_user.user_id
    pass

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, current_user: TokenData = Depends(get_current_user)):
    """
    Get a specific task, ensuring it belongs to the current user
    """
    # Verify that the task belongs to the current user
    # by querying database with both task_id and current_user.user_id
    # This implements database-level row security
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, current_user: TokenData = Depends(get_current_user)):
    """
    Update a specific task, ensuring it belongs to the current user
    """
    # Verify that the task belongs to the current user
    # by checking task.user_id == current_user.user_id
    pass

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: TokenData = Depends(get_current_user)):
    """
    Delete a specific task, ensuring it belongs to the current user
    """
    # Verify that the task belongs to the current user
    # by checking task.user_id == current_user.user_id
    pass

@router.patch("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int, complete_request: TaskComplete, current_user: TokenData = Depends(get_current_user)):
    """
    Toggle completion status of a task, ensuring it belongs to the current user
    """
    # Verify that the task belongs to the current user
    # by checking task.user_id == current_user.user_id
    pass
```

## Step 6: Implement Frontend Authentication Components

Create authentication components in your Next.js app:

```tsx
// components/LoginForm.tsx
'use client';

import { useState } from 'react';
import { useAuth } from 'better-auth/react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signIn?.({
        email,
        password,
      });
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

## Step 7: Configure HTTP Interceptors for JWT

Set up your frontend to automatically include JWT tokens in API requests:

```typescript
// lib/api-client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
});

// Request interceptor to include JWT token
apiClient.interceptors.request.use(
  (config) => {
    // Get JWT from Better Auth or httpOnly cookie
    // Note: With httpOnly cookies, the browser will automatically include them
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login page
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

## Step 8: Test the Integration

1. Start your backend server
2. Start your frontend development server
3. Register a new user
4. Log in with the new user
5. Create, read, update, and delete tasks
6. Verify that users cannot access each other's tasks
7. Test token expiration and refresh

## Troubleshooting

### Common Issues:
- **JWT validation failing**: Check that `BETTER_AUTH_SECRET` is the same in frontend and backend
- **httpOnly cookies not working**: Ensure your frontend and backend are on the same domain or properly configured for cross-origin requests
- **User isolation not working**: Verify that all database queries are filtered by the authenticated user ID

### Debugging Tips:
- Enable detailed logging in your JWT validation middleware
- Check that the `Authorization` header is properly formed (`Bearer <token>`)
- Verify that the JWT contains the expected claims (`sub`, `email`, etc.)

## Next Steps
- Implement token refresh mechanism
- Add more sophisticated error handling
- Set up proper session management
- Add unit and integration tests for authentication flow