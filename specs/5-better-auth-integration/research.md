# Research Document: Better Auth (JWT) Integration

## Overview
This document addresses the unknowns in the technical context for the Better Auth (JWT) Integration feature, resolving all "NEEDS CLARIFICATION" items.

## RQ-001: Better Auth Configuration

### Research Question
What is the proper configuration for Better Auth with JWT plugin in a Next.js frontend?

### Findings
Better Auth can be configured in Next.js using the following setup:

```javascript
import { BetterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = BetterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
    }),
  ],
  // Additional configuration options
});
```

### Decision
Configure Better Auth with JWT plugin using environment variables for secrets and proper database connection.

### Rationale
This approach follows Better Auth's recommended practices and allows for secure JWT handling with configurable algorithms.

### Alternatives Considered
- Custom JWT implementation (rejected - reinventing security wheel)
- Alternative auth providers (rejected - feature specifically requires Better Auth)

## RQ-002: JWT Token Structure

### Research Question
What is the JWT payload structure from Better Auth?

### Findings
Better Auth JWTs typically contain:
- `sub`: Subject (user ID)
- `iat`: Issued at time
- `exp`: Expiration time
- `email`: User email (optional)
- Custom claims can be added as needed

### Decision
Extract user ID from the `sub` claim and use additional claims as needed for application-specific data.

### Rationale
Following standard JWT claims ensures compatibility with existing JWT libraries and best practices.

### Alternatives Considered
- Storing user ID in custom claims (unnecessary for standard subject claim)
- Different token formats (JWT is required by specification)

## RQ-003: FastAPI JWT Middleware

### Research Question
How to implement JWT validation middleware in FastAPI?

### Findings
FastAPI supports JWT validation using python-jose library:

```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED

security = HTTPBearer()

def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token_payload = verify_jwt(credentials.credentials)
    return token_payload
```

### Decision
Implement JWT validation using python-jose library with proper exception handling.

### Rationale
This approach provides robust JWT validation with standard error handling patterns.

### Alternatives Considered
- PyJWT library (similar functionality, python-jose has better async support)
- Custom validation (security risk without proven library)

## RQ-004: User Data Isolation Patterns

### Research Question
Best practices for enforcing user data isolation in FastAPI with SQLModel.

### Findings
User data isolation should be implemented at multiple layers:
1. Application layer: Validate user ID in JWT against requested resource
2. Database layer: Always filter queries by user ID
3. API layer: Include user ID in all relevant endpoints

SQLModel example:
```python
# In route handler
def get_user_tasks(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user['sub'] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Query with user ID filter
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user['sub'])
    ).all()
```

### Decision
Implement dual-layer validation: API-level user ID checking and database-level filtering.

### Rationale
Defense in depth approach ensures security even if one layer fails.

### Alternatives Considered
- Only API-level validation (vulnerable to bypass)
- Only database-level filtering (less clear error handling)

## RQ-005: httpOnly Cookie Implementation

### Research Question
Secure httpOnly cookie implementation in Next.js with Better Auth.

### Findings
Better Auth handles httpOnly cookies automatically when configured properly. For Next.js App Router:

```javascript
// In layout.js or provider component
"use client";
import { BetterAuthProvider } from "better-auth/react";

export default function AuthProvider({ children }) {
  return (
    <BetterAuthProvider config={auth}>
      {children}
    </BetterAuthProvider>
  );
}
```

Better Auth will automatically store JWT in httpOnly cookies when configured with the JWT plugin.

### Decision
Use Better Auth's built-in httpOnly cookie handling with proper configuration.

### Rationale
Leverages well-tested, secure implementation from the auth library itself.

### Alternatives Considered
- Custom cookie implementation (unnecessary complexity)
- LocalStorage (vulnerable to XSS attacks)

## Summary
All research questions have been addressed and technical unknowns resolved. The implementation can proceed with confidence in the chosen approaches.



