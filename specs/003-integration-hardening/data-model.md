# Data Model: Integration, Hardening & Production Readiness

## Overview
Data model for the authenticated full-stack todo application focusing on entities and relationships with attention to data isolation and security.

## Core Entities

### User
Represents an authenticated user account with security and access controls.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `email`: String (Unique, Required, Email format validation)
- `hashed_password`: String (Required, Encrypted with bcrypt)
- `is_active`: Boolean (Default: true)
- `email_verified`: Boolean (Default: false)
- `created_at`: DateTime (Auto-generated on creation)
- `last_login`: DateTime (Nullable, Updated on each login)

**Relationships**:
- One-to-many with Task (user.tasks)

**Validation Rules**:
- Email must be unique and in valid format
- Account must be active to access system
- Password must be properly hashed before storage

### Task
Represents a todo item owned by a specific user with CRUD operations and completion tracking.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `title`: String (Required, Max length: 200 characters)
- `description`: String (Optional, Max length: 1000 characters)
- `completed`: Boolean (Default: false)
- `user_id`: Integer (Foreign Key to User.id, Required)
- `created_at`: DateTime (Auto-generated on creation)

**Relationships**:
- Many-to-one with User (task.user)

**Validation Rules**:
- Must belong to an active user
- User can only access tasks they own
- Title must not be empty

## State Transitions

### Task States
- **Pending**: `completed = false`, `created_at` set
- **Completed**: `completed = true`, `created_at` remains unchanged
- **Archived**: Deleted from active list (soft delete via status field in future)

### User States
- **Active**: `is_active = true`, can perform operations
- **Inactive**: `is_active = false`, blocked from operations
- **Verified**: `email_verified = true`, confirmed account
- **Unverified**: `email_verified = false`, unconfirmed account

## Security Constraints

### Access Control
- All task operations must validate user ownership
- API endpoints must verify authentication via JWT
- Database queries must filter by authenticated user ID
- No cross-user data access allowed

### Authentication Validation
- JWT token validation required for all protected endpoints
- Token payload must contain valid user ID
- Session validation on each request
- Automatic logout on token expiration

## Data Isolation Rules

### User Data Isolation
1. **Query Isolation**: All SELECT queries must include WHERE clause filtering by user_id
2. **Operation Isolation**: All CREATE/UPDATE/DELETE operations must verify user ownership
3. **Service Isolation**: Service layer must validate user_id matches authenticated user
4. **Presentation Isolation**: UI must only display user's own data

### Cross-Reference Validation
- Foreign key constraints enforced at database level
- Referential integrity maintained between User and Task
- Orphaned records prevented through cascade operations where appropriate

## API Contract Implications

### Request Validation
- User ID derived from JWT token, not request body (for protected operations)
- Input validation at API gateway level
- Sanitization of user input before database operations

### Response Format
- Consistent structure for all API responses
- Proper error codes and messages for all scenarios
- Minimal data exposure in responses
- Secure transmission of sensitive information

## Performance Considerations

### Indexing Strategy
- Index on User.email for login performance
- Index on Task.user_id for query filtering
- Composite indexes where appropriate for common queries

### Query Optimization
- Joins optimized for user-task relationships
- Pagination implemented for large datasets
- Caching considerations for frequently accessed data