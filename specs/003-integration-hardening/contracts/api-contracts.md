# API Contracts: Integration, Hardening & Production Readiness

## Overview
API contracts for the authenticated todo application with defined endpoints, request/response structures, and error handling patterns.

## Authentication Endpoints

### POST /api/auth/register
**Purpose**: Register a new user account

**Request**:
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required, min 8 chars)"
}
```

**Success Response (201)**:
```json
{
  "id": "integer",
  "email": "string",
  "is_active": "boolean",
  "email_verified": "boolean",
  "created_at": "ISO datetime string"
}
```

**Error Responses**:
- 400: Invalid input format or validation error
- 400: Email already registered
- 500: Server error during registration

---

### POST /api/auth/login
**Purpose**: Authenticate user and return JWT token

**Request**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Success Response (200)**:
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string ('bearer')",
  "user": {
    "id": "integer",
    "email": "string",
    "is_active": "boolean",
    "email_verified": "boolean",
    "created_at": "ISO datetime string"
  }
}
```

**Error Responses**:
- 400: Invalid input format
- 401: Incorrect email or password
- 500: Server error during authentication

---

### GET /api/auth/me
**Purpose**: Get current authenticated user information

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Success Response (200)**:
```json
{
  "id": "integer",
  "email": "string",
  "is_active": "boolean",
  "email_verified": "boolean",
  "created_at": "ISO datetime string"
}
```

**Error Responses**:
- 401: Missing or invalid token
- 500: Server error during user lookup

---

## Task Endpoints

### GET /api/tasks
**Purpose**: Retrieve all tasks for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Query Parameters**:
- `completed` (optional): boolean to filter by completion status

**Success Response (200)**:
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string (nullable)",
    "completed": "boolean",
    "created_at": "ISO datetime string",
    "user_id": "integer"
  }
]
```

**Error Responses**:
- 401: Missing or invalid token
- 500: Server error during task retrieval

---

### POST /api/tasks
**Purpose**: Create a new task for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Request**:
```json
{
  "title": "string (required)",
  "description": "string (optional)"
}
```

**Success Response (201)**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "ISO datetime string",
  "user_id": "integer"
}
```

**Error Responses**:
- 400: Invalid input format
- 401: Missing or invalid token
- 500: Server error during task creation

---

### GET /api/tasks/{id}
**Purpose**: Retrieve a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Parameters**:
- `id` (path): Task ID

**Success Response (200)**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "ISO datetime string",
  "user_id": "integer"
}
```

**Error Responses**:
- 401: Missing or invalid token
- 404: Task not found or does not belong to user
- 500: Server error during task retrieval

---

### PUT /api/tasks/{id}
**Purpose**: Update an existing task for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Parameters**:
- `id` (path): Task ID

**Request**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Success Response (200)**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "ISO datetime string",
  "user_id": "integer"
}
```

**Error Responses**:
- 400: Invalid input format
- 401: Missing or invalid token
- 404: Task not found or does not belong to user
- 500: Server error during task update

---

### DELETE /api/tasks/{id}
**Purpose**: Remove a task for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Parameters**:
- `id` (path): Task ID

**Success Response (200)**:
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401: Missing or invalid token
- 404: Task not found or does not belong to user
- 500: Server error during task deletion

---

### PATCH /api/tasks/{id}/complete
**Purpose**: Update task completion status for the authenticated user

**Headers**:
```
Authorization: Bearer <valid JWT token>
```

**Parameters**:
- `id` (path): Task ID

**Request**:
```json
{
  "completed": "boolean (required)"
}
```

**Success Response (200)**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "ISO datetime string",
  "user_id": "integer"
}
```

**Error Responses**:
- 400: Invalid input format
- 401: Missing or invalid token
- 404: Task not found or does not belong to user
- 500: Server error during task update

## Error Response Format

All error responses follow the standard format:
```json
{
  "detail": "Human-readable error message"
}
```

## Authentication Error Handling

- 401 Unauthorized: Token missing, invalid, or expired
- 403 Forbidden: Valid token but insufficient permissions
- 404 Not Found: Resource does not exist or does not belong to user
- 500 Internal Server Error: Unexpected server error

## Data Validation

- All inputs must be properly validated before processing
- Required fields must be present and non-empty
- Email fields must match valid email format
- Numeric fields must be within valid ranges
- String fields must respect character limits