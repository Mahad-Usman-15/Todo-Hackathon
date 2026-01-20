# Data Model: Better Auth (JWT) Integration

## Entities

### User
Represents an authenticated user with email, password, and associated tasks.

**Fields:**
- `id` (Integer, Primary Key, Auto-increment) - Unique identifier for the user
- `email` (String, Unique, Required) - User's email address for authentication
- `password_hash` (String, Required) - Hashed password for authentication
- `created_at` (DateTime, Required) - Timestamp when user was created
- `updated_at` (DateTime, Required) - Timestamp when user was last updated

**Relationships:**
- One-to-Many: User has many Tasks
- One-to-Many: User has many Sessions (if implementing custom session tracking)

**Validation Rules:**
- Email must be a valid email format
- Password must meet minimum strength requirements (handled by Better Auth)
- Email must be unique across all users

### JWT Token
Secure token issued by Better Auth containing user identity and expiration.

**Structure:**
- `sub` (Subject) - User ID
- `iat` (Issued At) - Token creation timestamp
- `exp` (Expiration) - Token expiration timestamp
- `email` (Optional) - User email

### Task
Todo item owned by a specific user with title, description, and completion status.

**Fields:**
- `id` (Integer, Primary Key, Auto-increment) - Unique identifier for the task
- `title` (String, Required) - Task title
- `description` (String, Optional) - Detailed description of the task
- `completed` (Boolean, Default: False) - Completion status
- `user_id` (Integer, Foreign Key) - Owner of the task
- `created_at` (DateTime, Required) - Timestamp when task was created
- `updated_at` (DateTime, Required) - Timestamp when task was last updated

**Relationships:**
- Many-to-One: Task belongs to User
- User owns many Tasks

**Validation Rules:**
- Title must not be empty
- User ID must correspond to an existing user
- Only the owner can modify the task
- All database queries must be filtered by authenticated user ID (row-level security)

### Session (Optional - if custom session tracking needed)
Represents an active authentication session for a user.

**Fields:**
- `id` (String, Primary Key) - Unique session identifier
- `user_id` (Integer, Foreign Key) - Associated user
- `expires_at` (DateTime) - Session expiration timestamp
- `created_at` (DateTime) - Session creation timestamp

**Relationships:**
- Many-to-One: Session belongs to User

## State Transitions

### User Authentication State
- `Unauthenticated` → `Authenticated` (on successful login)
- `Authenticated` → `Session Expired` (when JWT expires)
- `Session Expired` → `Unauthenticated` (on logout or forced expiration)

### Task Completion State
- `Incomplete` → `Complete` (when task is marked as done)
- `Complete` → `Incomplete` (when task is marked as undone)

## Constraints

### Security Constraints
- User ID in JWT token must match the user ID in the requested resource
- All task operations must be validated against the authenticated user
- Only the owner of a task can perform operations on it

### Data Integrity Constraints
- User email must be unique
- Task must have a valid user owner
- Created/updated timestamps are automatically managed

## Indexes
- User.email: Unique index for fast authentication lookups
- Task.user_id: Index for efficient user-specific task queries
- Session.expires_at: Index for session cleanup operations