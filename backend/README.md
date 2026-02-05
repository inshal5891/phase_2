# Todo Web Application - Backend

This is the backend for the secure todo web application built with FastAPI and SQLModel ORM.

## Features

- **RESTful API**: Full CRUD operations for tasks with proper HTTP status codes
- **Authentication**: JWT-based authentication with secure token generation
- **User Management**: User registration, login, and profile management
- **Data Isolation**: Each user can only access their own data
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM

## Architecture

### Models
- `User`: User accounts with authentication fields (email, hashed password, etc.)
- `Task`: Task entities associated with users via foreign key

### Services
- `UserService`: Handles user registration, authentication, and management
- `TaskService`: Handles task creation, retrieval, updating, and deletion with user isolation

### Authentication
- `auth/security.py`: JWT token creation and verification
- `auth/dependencies.py`: FastAPI dependencies for authentication
- `auth/middleware.py`: Authentication middleware (if needed)

### API Routes
- `/api/auth/register`: User registration
- `/api/auth/login`: User authentication
- `/api/auth/me`: Get current user info
- `/api/tasks`: Task management endpoints (all require authentication)

## Security Features

- JWT token verification on all protected endpoints
- User ID extraction from JWT tokens
- Automatic user data filtering - users only see their own tasks
- Password hashing with bcrypt
- Secure token generation with expiration

## Environment Variables

- `DATABASE_URL`: Neon Serverless PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: Algorithm for JWT token encoding (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Start the server: `uvicorn main:app --reload`
4. Visit `http://localhost:8000/docs` for API documentation

All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```