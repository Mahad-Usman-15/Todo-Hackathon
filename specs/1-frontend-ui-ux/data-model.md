# Data Model: Frontend Web Application — Professional UI/UX

## Task Entity (Frontend Types)

### Task Interface
```typescript
interface Task {
  id: string;              // Unique identifier for the task
  title: string;           // Task title (required, max 100 chars)
  description?: string;    // Optional task description (max 500 chars)
  completed: boolean;      // Task completion status
  createdAt: string;       // ISO date string when task was created
  updatedAt: string;       // ISO date string when task was last updated
  userId: string;          // User ID (for data isolation)
}
```

### Task Creation Input
```typescript
interface CreateTaskInput {
  title: string;           // Required, max 100 chars
  description?: string;    // Optional, max 500 chars
  completed?: boolean;     // Defaults to false
}
```

### Task Update Input
```typescript
interface UpdateTaskInput {
  title?: string;          // Optional, max 100 chars
  description?: string;    // Optional, max 500 chars
  completed?: boolean;     // Optional completion status
}
```

## User Authentication Entity

### User Interface
```typescript
interface User {
  id: string;              // User unique identifier
  email: string;           // User email address
  name?: string;           // Optional user display name
}
```

### Authentication State
```typescript
interface AuthState {
  user: User | null;       // Current authenticated user
  token: string | null;    // JWT token
  isAuthenticated: boolean; // Authentication status
  isLoading: boolean;      // Auth state loading status
}
```

## API Response Types

### Task API Response
```typescript
interface TaskApiResponse {
  data: Task | Task[];     // Single task or array of tasks
  message?: string;        // Optional response message
  error?: string;          // Optional error message
}
```

### Authentication API Response
```typescript
interface AuthApiResponse {
  user: User;              // Authenticated user data
  token: string;           // JWT token
  message?: string;        // Optional response message
}
```

## UI State Models

### Task List State
```typescript
interface TaskListState {
  tasks: Task[];           // Array of tasks
  loading: boolean;        // Loading state
  error: string | null;    // Error state
  filter: 'all' | 'active' | 'completed'; // Task filter
}
```

### Form State
```typescript
interface FormState {
  title: string;           // Current title value
  description: string;     // Current description value
  errors: {               // Form validation errors
    title?: string;
    description?: string;
  };
  isSubmitting: boolean;   // Form submission state
}
```

## Validation Rules

### Task Validation
- Title: Required, 1-100 characters
- Description: Optional, 0-500 characters
- Completed: Boolean, defaults to false
- All string fields must be trimmed

### Form Validation
- Title must not be empty or whitespace-only
- Title must not exceed 100 characters
- Description must not exceed 500 characters
- Real-time validation feedback for better UX

## API Contract Mapping

### Frontend to Backend Mapping
The frontend will map to the backend API as specified in the constitution:

- GET `/api/{user_id}/tasks` → FetchTaskList
- POST `/api/{user_id}/tasks` → CreateTask
- GET `/api/{user_id}/tasks/{id}` → FetchTask
- PUT `/api/{user_id}/tasks/{id}` → UpdateTask
- DELETE `/api/{user_id}/tasks/{id}` → DeleteTask
- PATCH `/api/{user_id}/tasks/{id}/complete` → ToggleTaskCompletion

### Error Handling Types
```typescript
enum ApiErrorType {
  UNAUTHORIZED = 'UNAUTHORIZED',     // 401 - Invalid or missing JWT
  FORBIDDEN = 'FORBIDDEN',          // 403 - Access to resource denied
  NOT_FOUND = 'NOT_FOUND',          // 404 - Resource not found
  VALIDATION_ERROR = 'VALIDATION_ERROR', // 422 - Validation failed
  SERVER_ERROR = 'SERVER_ERROR',    // 500 - Server error
  NETWORK_ERROR = 'NETWORK_ERROR'   // Network connectivity issue
}
```

## State Management

### Global State Structure
The frontend will use React Context or similar for state management:

- Authentication state: User session and token
- Task state: Current tasks, filters, loading states
- UI state: Modals, notifications, form states
- Error state: Application-level error handling

### Component State Patterns
- Form components: Local state with validation
- Interactive components: Local state for UI interactions
- Data-fetching components: Local state for loading/error states
- Layout components: Local state for responsive behavior