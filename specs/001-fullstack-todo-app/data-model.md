# Data Model: Core Full-Stack Todo Web Application

## Entity Definitions

### Task Entity
**Description**: Represents a todo item with attributes including ID, title, description, completion status, and creation timestamp

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String (Required, Max length: 255)
- `description`: String (Optional, Max length: 1000)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Default: Current timestamp)
- `user_id`: Integer (Foreign Key to User, indexed)

**Validation Rules**:
- Title must not be empty
- Title must be between 1-255 characters
- Description can be null or 1-1000 characters
- Completed defaults to False if not specified

**State Transitions**:
- Pending → Completed: When user marks task as complete
- Completed → Pending: When user unmarks task completion

### User Entity (Logical Context)
**Description**: Represents a logical user context for organizing tasks (handled without authentication in this spec)

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `email`: String (Unique, for logical identification)
- `created_at`: DateTime (Default: Current timestamp)

**Note**: Authentication/authorization is deferred to Spec 2; currently only used for data isolation.

## Relationships

### Task ↔ User
- **Relationship**: Many-to-One (Many tasks belong to one user)
- **Cardinality**: Each task belongs to exactly one user; each user can have zero or many tasks
- **Constraint**: Foreign key constraint ensures referential integrity

## Database Schema

```sql
-- Users table (logical context only, no auth in this spec)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Index for performance on user_id
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for performance on completed status
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## API Data Contracts

### Request/Response Objects

#### Task Creation Request
```json
{
  "title": "String (required)",
  "description": "String (optional)"
}
```

#### Task Response Object
```json
{
  "id": "Integer",
  "title": "String",
  "description": "String (can be null)",
  "completed": "Boolean",
  "created_at": "ISO 8601 DateTime String",
  "user_id": "Integer"
}
```

#### Task Update Request
```json
{
  "title": "String (optional)",
  "description": "String (optional)",
  "completed": "Boolean (optional)"
}
```

#### Task List Response
```json
[
  {
    "id": "Integer",
    "title": "String",
    "description": "String (can be null)",
    "completed": "Boolean",
    "created_at": "ISO 8601 DateTime String",
    "user_id": "Integer"
  }
]
```

## Validation Rules

### Backend Validation
- All incoming data must be validated against Pydantic models
- Title field required and 1-255 characters
- Description field optional, max 1000 characters
- User ID must correspond to an existing user record
- Task ID must correspond to an existing task for update/delete operations

### Frontend Validation
- Form validation before submission
- Input sanitization for security
- Display validation errors to user

## Business Logic Constraints

1. **Data Integrity**: Tasks must always belong to a valid user
2. **Soft Deletes**: Instead of permanent deletion, tasks could be marked as archived (future enhancement)
3. **Timestamp Immutability**: Created timestamp cannot be modified after creation
4. **User Isolation**: Users can only access their own tasks (enforced at API level)

## Performance Considerations

1. **Indexing**: Index on user_id for efficient user-based queries
2. **Query Optimization**: Use proper JOINs and filtering at database level
3. **Pagination**: Implement pagination for task lists to handle large datasets
4. **Connection Pooling**: Use database connection pooling for performance