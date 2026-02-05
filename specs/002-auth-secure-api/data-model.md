# Data Model: Authentication & Secure API Access

## Entity Definitions

### User Entity (Updated)
**Description**: Represents a registered user with authentication-specific fields in addition to the original user context from Spec 1

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `email`: String (Unique, Required, Max length: 255) - Original email field from Spec 1, enhanced with uniqueness constraint
- `hashed_password`: String (Required, Max length: 255) - BCrypt hashed password
- `is_active`: Boolean (Default: True) - Account status flag
- `email_verified`: Boolean (Default: False) - Email verification status
- `created_at`: DateTime (Default: Current timestamp) - Original created_at field from Spec 1
- `last_login`: DateTime (Nullable) - Timestamp of last successful login

**Validation Rules**:
- Email must be valid email format and unique across all users
- Email must not be empty and be between 5-255 characters
- Hashed password must be present (after bcrypt hashing)
- is_active defaults to True when creating account
- Email must be unique across all users

**State Transitions**:
- Unverified → Verified: When user confirms email verification
- Active → Inactive: When account is suspended/deactivated
- Inactive → Active: When account is reactivated

## Enhanced Task Entity (from Spec 1)
**Description**: Updated to enforce user ownership and authentication-based access

**Additional Constraints** (beyond Spec 1):
- Foreign key relationship to User entity (user_id) becomes the primary mechanism for data isolation
- All task operations (CRUD) are filtered by authenticated user's ID

## JWT Token Structure

### Access Token Claims
**Description**: JWT access token issued upon successful authentication

**Claims**:
- `sub`: Subject (User ID)
- `exp`: Expiration time (Unix timestamp)
- `iat`: Issued at time (Unix timestamp)
- `jti`: JWT ID for revocation tracking (optional)
- `user_id`: User identifier for easy access
- `email`: User's email (for convenience)

**Token Properties**:
- Algorithm: RS256 (recommended) or HS256
- Expiration: 30 minutes from issue (configurable)
- Refresh token: 7 days from issue (optional, for future enhancement)

## Session/Authentication State

### Authenticated Request Context
**Description**: Contextual information available for each authenticated request

**Properties**:
- `user_id`: Authenticated user's ID extracted from JWT
- `user_email`: Authenticated user's email for logging/debugging
- `permissions`: User's permission level (currently all users have same basic permissions)
- `request_timestamp`: When the request was made
- `session_id`: Identifier for tracking request session (optional)

## Database Schema Changes

### User Table (Extends existing from Spec 1)
```sql
-- Updates to existing users table from Spec 1
ALTER TABLE users
ADD COLUMN hashed_password VARCHAR(255) NOT NULL,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE,
ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN last_login TIMESTAMP NULL;

-- Ensure email uniqueness
ALTER TABLE users ADD CONSTRAINT uk_users_email UNIQUE (email);
```

### Security Considerations
- Passwords must never be stored in plain text
- Hashed passwords should use bcrypt with at least 12 rounds
- JWT secrets should be stored in environment variables, never committed to code
- Access tokens should have short expiration times
- Consider rate limiting authentication attempts

## API Data Contracts

### Authentication Request/Response Objects

#### User Registration Request
```json
{
  "email": "String (required, valid email format)",
  "password": "String (required, min 8 characters with complexity)"
}
```

#### User Registration Response
```json
{
  "id": "Integer",
  "email": "String",
  "created_at": "ISO 8601 DateTime String",
  "email_verified": "Boolean",
  "is_active": "Boolean"
}
```

#### Login Request
```json
{
  "email": "String (required)",
  "password": "String (required)"
}
```

#### Login Response
```json
{
  "access_token": "JWT String",
  "token_type": "String (always 'bearer')",
  "user": {
    "id": "Integer",
    "email": "String",
    "is_active": "Boolean"
  }
}
```

#### Authenticated Request (All existing endpoints now require this)
```json
{
  "headers": {
    "Authorization": "Bearer {jwt_token}"
  }
}
```

## Validation Rules

### Backend Validation
- All authentication input must be validated for proper format and security requirements
- Passwords must meet complexity requirements (min 8 characters, mixed case, numbers, special chars)
- Email must pass RFC-compliant validation
- JWT tokens must be properly formatted and not expired
- User accounts must be active to authenticate
- All requests to task endpoints must include valid JWT

### Frontend Validation
- Form validation before authentication requests
- Secure storage of tokens (httpOnly cookies or secure localStorage)
- Proper handling of authentication errors
- Automatic redirection to login when tokens expire

## Business Logic Constraints

1. **Authentication Required**: All task operations require valid authentication token
2. **Data Isolation**: Users can only access tasks associated with their user ID
3. **Secure Passwords**: Passwords must be properly hashed before storing
4. **Token Validation**: JWT tokens must be validated with correct secret
5. **Rate Limiting**: Authentication attempts should be rate-limited to prevent brute force
6. **Account Security**: Suspended accounts cannot authenticate

## Performance Considerations

1. **Token Validation Efficiency**: JWT validation should be efficient (avoid database lookups if possible)
2. **Password Verification**: Bcrypt verification should use appropriate rounds for security vs performance balance
3. **Database Indexing**: User email should be indexed for quick lookup during authentication
4. **Caching**: Consider caching validated JWTs for repeated requests within a session
5. **Connection Pooling**: Maintain database connection pools for authentication-related queries