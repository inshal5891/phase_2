# Phase II - Todo Web Application: Integration, Hardening & Production Readiness

This repository contains a full-stack todo web application with authentication and secure API access, representing Phase II of the project. The application has been integrated, hardened, and prepared for production readiness.

## Features

- **Full-Stack Todo Application**: Complete CRUD functionality for todo items
- **User Authentication**: Secure signup and login with JWT tokens
- **Data Isolation**: Each user can only access their own tasks
- **Responsive UI**: Modern web interface built with Next.js
- **RESTful API**: Well-designed API endpoints with proper HTTP status codes
- **Database Integration**: Neon Serverless PostgreSQL with SQLModel ORM

## Architecture

### Tech Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.12
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based with custom security implementation
- **State Management**: React Context for authentication state

### System Flow
```
User → Frontend (Auth + UI) → JWT → FastAPI Middleware → Service Layer → DB → Response → UI
```

## Environment Configuration

### Backend Configuration

Copy `.env.example` to `.env` and set your environment variables:

```bash
cp backend/.env.example backend/.env
```

Configure the following variables:
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (change for production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `APP_ENV`: Environment (development/production)
- `DEBUG`: Enable/disable debug mode

### Frontend Configuration

Copy `.env.local.example` to `.env.local` and set your environment variables:

```bash
cp frontend/.env.local.example frontend/.env.local
```

Configure the following variables:
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (default: http://localhost:8000/api)

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn
- Neon Serverless PostgreSQL account

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables (see above)

4. Start the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables (see above)

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Security Features

- **JWT Token Authentication**: All API endpoints require valid JWT tokens
- **User Data Isolation**: Each user can only access their own tasks
- **Secure Token Storage**: JWT tokens stored securely in browser's localStorage
- **Automatic Expiration**: Tokens automatically expire after configured time
- **Proper Error Handling**: Consistent error responses with appropriate status codes

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Tasks
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Update completion status

## User Flows

### Complete End-to-End Flow
1. User signs up for an account
2. User logs in and receives JWT token
3. User can create, read, update, and delete their tasks
4. User can log out, clearing their session

### Error Handling
- Invalid credentials show clear error messages
- Expired tokens redirect to login page
- Unauthorized access to protected resources redirects to login
- All error states are handled gracefully with user feedback

## Development Workflow

This project follows an agentic development approach:
- **Specification Phase** (`/sp.specify`): Define requirements and user stories
- **Planning Phase** (`/sp.plan`): Create technical architecture and data models
- **Task Breakdown Phase** (`/sp.tasks`): Split implementation into testable tasks
- **Implementation Phase** (`/sp.implement`): Execute tasks and build features

## Running Tests

Backend tests:
```bash
cd backend
pytest
```

## Production Deployment

For production deployment:
1. Use secure values for all environment variables
2. Set `APP_ENV=production` and `DEBUG=False`
3. Configure SSL for HTTPS
4. Implement proper logging
5. Set up monitoring and alerting

## Development Notes

This project was built using an agent-driven development approach following the Spec-Kit methodology:
- Specification (spec) → Planning (plan) → Tasks (tasks) → Implementation (implement)

The implementation is divided into phases:
- Phase 1: Core full-stack todo application
- Phase 2: Authentication and secure API access
- Phase 3: Integration, hardening, and production readiness (current phase)

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure your Neon PostgreSQL connection string is correct
- **JWT Secret**: Make sure the same secret is used in both backend and any frontend validation
- **CORS**: Check if your frontend domain is allowed in the backend CORS settings
- **Environment Variables**: Verify all environment variables are set correctly

### API Documentation
The backend includes automatic API documentation at `/docs` when running in development mode.