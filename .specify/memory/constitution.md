<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.1
- Modified principles: Consolidated duplicate principles
- Removed sections: Duplicate Core Principles section
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->

# Todo App Phase II Constitution

## Core Principles

### I. Spec-First Development
Always read and obey specs before implementation. Reference specs using `@specs/...` paths. If a requirement is unclear, update or request a spec — never guess.

### II. Agentic Dev Stack Workflow (MANDATORY)
Execute work strictly in this order:
1. Read relevant specs
2. Generate an implementation plan
3. Break plan into concrete tasks
4. Implement tasks incrementally
5. Validate against acceptance criteria

Skipping steps is forbidden.

### III. No Manual Coding
All code must be generated as part of the agentic workflow. No shortcuts, no partial implementations.

### IV. Security-First Architecture
Security must be considered at every layer of the application. Authentication and authorization are non-negotiable requirements for all features.

### V. Full-Stack Integration
The frontend and backend must work seamlessly together with consistent data models and API contracts. All components must be designed for integration from the start.

### VI. User Data Isolation
User data must be strictly isolated. No user should have access to another user's data under any circumstances.

## Additional Constraints

### Technology Stack (STRICT)
#### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Shadcn/ui
#### Backend
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL

#### Architecture
- Monorepo
- Spec-Kit Plus driven
- Shared JWT secret via environment variable

### Authentication & Security (CRITICAL)
#### Authentication Model
- Better Auth runs on the frontend
- JWT tokens are issued on login
- JWT is sent with every API request:
`Authorization: Bearer <token>`

#### Backend Requirements
- Verify JWT signature using `BETTER_AUTH_SECRET`
- Extract authenticated user ID from token
- Enforce **strict user isolation**
- Reject unauthenticated requests with `401 Unauthorized`

#### Security Rules
- Every API operation must validate task ownership
- Never trust `user_id` from request without JWT verification
- All task queries must be filtered by authenticated user

### API Contract (MUST MATCH SPECS)
All endpoints:
- Require valid JWT
- Return JSON
- Enforce per-user data isolation

#### Endpoints
- GET    `/api/{user_id}/tasks`
- POST   `/api/{user_id}/tasks`
- GET    `/api/{user_id}/tasks/{id}`
- PUT    `/api/{user_id}/tasks/{id}`
- DELETE `/api/{user_id}/tasks/{id}`
- PATCH  `/api/{user_id}/tasks/{id}/complete`

### Database Rules
- Use SQLModel exclusively
- PostgreSQL via Neon Serverless
- Schema defined in `@specs/database/schema.md`
- All tasks must include:
  - `user_id`
  - ownership enforcement at query level

### Frontend Rules
- Server Components by default
- Client Components only when required
- All API calls go through a centralized API client
- JWT token must be attached to every request
- UI must be responsive and user-friendly

### Backend Rules
- FastAPI only
- Routes under `/api/`
- Pydantic request/response models
- Clear HTTP error handling
- JWT verification middleware required

## Development Workflow
You must always consult and obey:
- `@specs/overview.md`
- `@specs/features/task-crud.md`
- `@specs/features/authentication.md`
- `@specs/api/rest-endpoints.md`
- `@specs/database/schema.md`
- Root, frontend, and backend `CLAUDE.md` files

If specs conflict, **pause and request clarification**.

For every task you perform, you must:
1. State which specs you are using
2. Present a clear plan
3. Execute implementation step-by-step
4. Ensure code compiles and follows stack rules
5. Confirm acceptance criteria are met

## Governance

This constitution supersedes all other practices; Amendments require documentation and approval following the `/sp.constitution` workflow; All implementations must verify compliance with these principles; Versioning follows semantic versioning with MAJOR for breaking governance changes, MINOR for new principles, PATCH for clarifications.

**Version**: 1.0.1 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03