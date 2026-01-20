# Implementation Plan: Better Auth (JWT) Integration

## Technical Context

**Feature**: Better Auth (JWT) Integration into Existing Todo App Monorepo
**Branch**: 5-better-auth-integration
**Dependencies**: Better Auth, JWT, Next.js, FastAPI, Neon PostgreSQL
**Integration Points**: Frontend authentication, Backend JWT validation, User data isolation

### Current State
- Existing todo app without proper authentication
- Need to integrate Better Auth with JWT for secure user sessions
- Backend needs to validate JWT tokens and enforce user isolation

### Target State
- Full Better Auth integration with JWT
- Secure token storage using httpOnly cookies
- Backend validation of all requests with user data isolation
- Automatic token refresh mechanism

### Unknowns
- Specific Better Auth configuration options - RESOLVED in research.md
- JWT payload structure from Better Auth - RESOLVED in research.md
- How to integrate with existing API routes - RESOLVED in research.md
- Database schema for user management - RESOLVED in research.md

## Constitution Check

Based on `.specify/memory/constitution.md`, this implementation must:
- ✅ Follow Spec-First Development (using feature spec)
- ✅ Implement Security-First Architecture (proper auth/authz)
- ✅ Ensure Full-Stack Integration (consistent data models)
- ✅ Enforce User Data Isolation (strict per-user data separation)
- ✅ Use prescribed tech stack (Next.js, FastAPI, Better Auth, Neon PG)
- ✅ Follow authentication requirements (JWT validation, 401 responses)
- ✅ Implement API contracts as specified

## Gates

### Prerequisites
- [x] Better Auth configured with JWT plugin (research completed)
- [x] BETTER_AUTH_SECRET environment variable available to both frontend and backend (research completed)
- [x] Existing API routes identified for integration (research completed)
- [x] Database schema updated to support user management (research completed)

### Success Criteria
- [x] All API endpoints require valid JWT tokens (defined in contracts)
- [x] User data isolation enforced at backend level (defined in contracts)
- [x] JWT tokens stored securely in httpOnly cookies (defined in contracts)
- [x] Automatic token refresh implemented (defined in contracts)
- [x] Error handling provides user-friendly messages (defined in contracts)

### Risk Assessment
- High: Security vulnerabilities if JWT validation is not properly implemented
- High: Data leakage if user isolation is not enforced correctly
- Medium: Breaking changes to existing API routes
- Low: Performance impact from token validation overhead

### Gate Status
✅ All gates passed - implementation can proceed based on completed research

---

## Phase 0: Research & Discovery

### Research Tasks

#### RT-001: Better Auth Configuration
- **Objective**: Research Better Auth setup with JWT plugin for Next.js frontend
- **Resources**: Better Auth documentation, JWT plugin configuration
- **Deliverable**: Configuration guide for frontend integration

#### RT-002: JWT Token Structure
- **Objective**: Understand JWT payload structure from Better Auth
- **Resources**: Better Auth docs, JWT standards
- **Deliverable**: JWT payload schema and extraction methods

#### RT-003: FastAPI JWT Middleware
- **Objective**: Research JWT validation implementation in FastAPI
- **Resources**: FastAPI documentation, JWT libraries for Python
- **Deliverable**: Middleware implementation approach

#### RT-004: User Data Isolation Patterns
- **Objective**: Research best practices for enforcing user data isolation in FastAPI with SQLModel
- **Resources**: FastAPI security guides, SQLModel documentation
- **Deliverable**: Data isolation implementation patterns

#### RT-005: httpOnly Cookie Implementation
- **Objective**: Research secure httpOnly cookie implementation in Next.js
- **Resources**: Next.js documentation, Better Auth cookie handling
- **Deliverable**: Cookie storage and retrieval implementation

## Phase 1: Design & Architecture

### D-001: Data Model Design
- **Entity**: User (email, password hash, created_at, updated_at)
- **Relationship**: User has many Tasks
- **Validation**: Email format, password strength
- **State Transitions**: Unauthenticated → Authenticated → Session Expired

### D-002: API Contract Design
- **POST** `/api/auth/register` - Register new user
- **POST** `/api/auth/login` - Login existing user
- **POST** `/api/auth/logout` - Logout current user
- **GET** `/api/tasks` - Get current user's tasks (with JWT validation)
- **POST** `/api/tasks` - Create task for current user (with JWT validation)
- **GET** `/api/tasks/{id}` - Get specific task (with ownership validation)
- **PUT** `/api/tasks/{id}` - Update specific task (with ownership validation)
- **DELETE** `/api/tasks/{id}` - Delete specific task (with ownership validation)
- **PATCH** `/api/tasks/{id}/complete` - Toggle task completion (with ownership validation)

### D-003: Authentication Flow Design
1. User visits app and is unauthenticated
2. User registers or logs in via Better Auth
3. Better Auth sets httpOnly cookie with JWT
4. Frontend makes API calls with JWT from cookie
5. Backend validates JWT and extracts user ID
6. Backend enforces user data isolation based on extracted user ID

### D-004: Security Implementation
- JWT validation middleware in FastAPI
- User ID extraction from JWT claims
- Ownership validation in all task operations at both API and database levels
- Database query filtering by authenticated user ID
- Proper error responses (401, 403, 404)

## Phase 2: Implementation Plan

### IP-001: Frontend Better Auth Setup
- Set up Better Auth provider in Next.js app
- Configure JWT plugin
- Implement httpOnly cookie storage
- Create login/logout components

### IP-002: Backend JWT Validation Middleware
- Implement JWT validation middleware in FastAPI
- Extract user ID from JWT claims
- Add user ID to request context
- Return 401 for invalid tokens

### IP-003: User Data Isolation Enforcement
- Modify all task endpoints to validate ownership
- Add user ID filters to all database queries
- Implement proper error responses (403 for unauthorized access)

### IP-004: API Integration
- Integrate JWT validation with existing task endpoints
- Update API clients to include JWT tokens
- Handle 401 responses with redirect to login

### IP-005: Token Refresh Mechanism
- Implement automatic token refresh
- Handle expired token scenarios
- Fallback to login redirect when refresh fails

## Phase 3: Testing & Validation

### TV-001: Authentication Flow Testing
- Test user registration flow
- Test login/logout functionality
- Test JWT token generation and storage

### TV-002: Authorization Testing
- Test user data isolation
- Verify 401 responses for unauthenticated requests
- Verify 403 responses for unauthorized access

### TV-003: End-to-End Testing
- Complete user journey: register → login → create tasks → logout
- Test token refresh functionality
- Test error handling scenarios

## Quickstart Guide

1. Install Better Auth and JWT plugin dependencies
2. Configure BETTER_AUTH_SECRET environment variable
3. Set up Better Auth provider in Next.js app
4. Implement JWT validation middleware in FastAPI
5. Update all task endpoints with user data isolation
6. Test authentication flow end-to-end