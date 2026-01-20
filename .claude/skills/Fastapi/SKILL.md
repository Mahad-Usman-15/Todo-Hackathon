---
name: fastapi-code-writer
description: A skill for generating FastAPI code and logic based on specifications, ensuring best practices for API endpoints, models, routers, and integrations (e.g., ORM, auth).
version: 1.0
---

## When to Use This Skill
Use this skill when:
- Implementing or updating backend API logic in FastAPI, such as endpoints, routers, models, or middleware.
- The task involves 3+ decision points (e.g., handling requests/responses, database integration, error handling, security).
- Working in a Spec-Driven Development (SDD) context, where code must align with specs (e.g., @specs/api/rest-endpoints.md).
- Repeating similar patterns across projects (e.g., CRUD operations, JWT auth in monorepos).
- Do NOT use for trivial tasks like basic imports or non-FastAPI code (e.g., pure Python scripts).

Triggers: User requests like "Implement a POST endpoint for creating tasks" or "Generate FastAPI router for user authentication."

## Process Steps
Follow these steps sequentially to generate the code:

1. **Read Relevant Specs**: Load and review the provided spec(s) (e.g., @specs/api/rest-endpoints.md or @specs/database/schema.md). Extract key details like endpoint methods, request/response models, authentication requirements, and data filtering (e.g., user isolation).

2. **Plan the Structure**: Outline the code components needed:
   - Imports (e.g., from fastapi, sqlmodel, pydantic).
   - Models (e.g., Pydantic for requests, SQLModel for DB).
   - Dependencies (e.g., JWT verification middleware).
   - Router/Endpoint logic (e.g., async def with response models).
   - Error handling (e.g., HTTPException for 404, 401).
   - Integration points (e.g., DB session, auth user extraction).

3. **Generate the Code**: Write the FastAPI code in Python, adhering to conventions:
   - Use APIRouter for modularity.
   - Include type hints and response models.
   - Enforce security (e.g., verify JWT, filter by user_id).
   - Handle edge cases (e.g., validation, duplicates).
   - Follow backend/CLAUDE.md guidelines if in a monorepo (e.g., routes under /api/, JSON responses).

4. **Add Explanations**: Inline comments in the code for key decisions, and a summary of how it aligns with the spec.

5. **Quality Check**: Validate against criteria below. If not met, iterate (e.g., revise for missing auth).

## Output Format
- **Code Block**: The generated Python code in a fenced code block (```python).
- **Explanations**: Bullet points below the code explaining key choices and spec alignment.
- **File Placement Suggestions**: Where to place the code in the monorepo (e.g., backend/routes/tasks.py).
- **Dependencies**: List any required env vars or packages (e.g., BETTER_AUTH_SECRET).

## Quality Criteria
The output is "ready" if:
- Code is syntactically correct, follows FastAPI best practices (e.g., async, dependency injection).
- Fully aligns with the input spec (e.g., exact endpoints, data models).
- Includes security (e.g., JWT verification, user filtering) and error handling.
- Modular and readable (e.g., <200 lines per file, clear comments).
- No vulnerabilities (e.g., SQL injection via SQLModel).
- Tested mentally for edge cases (e.g., invalid input returns 422).

If any criterion fails (e.g., missing user isolation), mark as "needs work" and suggest fixes.

## Example
### Input
Implement the POST /api/{user_id}/tasks endpoint based on @specs/api/rest-endpoints.md. It should create a new task for the authenticated user, using SQLModel for DB, and verify JWT.

### Output
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.db import get_session
from backend.models import Task, TaskCreate
from backend.auth import get_current_user

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.post("/", response_model=Task)
async def create_task(
    user_id: str,
    task: TaskCreate,
    db: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task