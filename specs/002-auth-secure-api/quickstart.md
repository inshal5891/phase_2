# Quickstart Guide: Authentication & Secure API Access

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.12+ for backend development
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Git for version control
- Access to Claude Code agents (frontend, backend, database, auth)

## Setup Instructions

### 1. Clone and Navigate to Repository

```bash
git clone <repository-url>
cd <repository-name>
git checkout 002-auth-secure-api  # Use the feature branch
```

### 2. Backend Setup (FastAPI + Better Auth + JWT)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# If requirements.txt doesn't exist yet, install the base dependencies:
pip install fastapi uvicorn sqlmodel psycopg[binary] python-dotenv python-jose[cryptography] passlib[bcrypt] pytest httpx python-multipart

# Set up environment variables
cp .env.example .env
# Edit .env with your database connection and JWT secret:
# DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
# BETTER_AUTH_SECRET=your-secret-key-for-jwt-signing
# ALGORITHM=RS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Frontend Setup (Next.js 16+ with Better Auth)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Install Better Auth dependencies
npm install better-auth @better-auth/react

# Set up environment variables
cp .env.local.example .env.local
# Configure API endpoints and auth settings:
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 4. Database Initialization

```bash
# From backend directory
cd src

# Initialize the database tables (including user table with auth fields)
python -c "
from backend.database.session import engine
from backend.models import user, task
from sqlmodel import SQLModel

# Create all tables including updated user model
SQLModel.metadata.create_all(engine)
print('Database tables with authentication fields created successfully')
"
```

## Running the Application with Authentication

### 1. Start Backend Server

```bash
# From backend directory
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000` with authentication-enabled endpoints.

### 2. Start Frontend Server

```bash
# From frontend directory
cd frontend
npm run dev
# or
yarn dev
```

Frontend will be available at `http://localhost:3000`

## Authentication API Endpoints

Once running, the following authentication endpoints will be available:

```
POST   /auth/register        # Register a new user
POST   /auth/login          # Authenticate user and return JWT
POST   /auth/logout         # Logout user
GET    /auth/me             # Get authenticated user info
POST   /auth/change-password # Change authenticated user's password
```

## Updated Protected Task Endpoints

All existing task endpoints now require JWT authentication:

```
GET    /api/tasks          # Get authenticated user's tasks
POST   /api/tasks          # Create task for authenticated user
GET    /api/tasks/{id}     # Get specific task (must belong to user)
PUT    /api/tasks/{id}     # Update task (must belong to user)
DELETE /api/tasks/{id}     # Delete task (must belong to user)
PATCH  /api/tasks/{id}/complete  # Toggle completion status (must belong to user)
```

## Development Workflow

1. **Architecture Decisions**: Document any significant changes in Architecture Decision Records (ADRs)
2. **Task Creation**: Use `/sp.tasks` to generate implementation tasks from the plan
3. **Agent Utilization**:
   - Use `auth-security-specialist` for authentication features (required for this spec)
   - Use `nextjs-ui-optimizer` for frontend auth components
   - Use `fastapi-backend-engineer` for API endpoints with JWT middleware
   - Use `neon-db-manager` for database schema updates (user auth fields)
4. **Testing**: Run authentication tests after implementing auth features:
   ```bash
   # Backend authentication tests
   pytest tests/auth/

   # Frontend auth tests
   npm run test -- src/app/auth/
   ```

## Common Commands

```bash
# Generate tasks from plan
/sp.tasks

# Run backend authentication tests
cd backend && pytest tests/auth/

# Run frontend auth tests
cd frontend && npm run test -- src/app/auth/

# Check backend API docs (includes authentication endpoints)
http://localhost:8000/docs

# Format code
cd backend && black src/
cd frontend && npm run format
```

## Environment Configuration

### Backend Environment Variables
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `ALGORITHM` - JWT algorithm (RS256 recommended)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `DATABASE_URL` - PostgreSQL database connection string
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration time (optional)

### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Better Auth server URL
- `NEXT_PUBLIC_JWT_NAME` - Name for the JWT cookie (optional)

## Troubleshooting

### Authentication Issues
- Verify `BETTER_AUTH_SECRET` is consistent between frontend and backend
- Check that JWT tokens are properly included in Authorization headers
- Confirm that user accounts are active and email is verified

### Database Connection Issues
- Verify `DATABASE_URL` in environment variables
- Ensure Neon PostgreSQL is active and accessible
- Check that user table has been updated with authentication fields

### Frontend Cannot Reach Backend Auth
- Verify `NEXT_PUBLIC_API_BASE_URL` is correctly set
- Check CORS settings in FastAPI backend for auth endpoints
- Ensure both servers are running simultaneously

### Dependency Issues
- Backend: Reinstall with `pip install -r requirements.txt --force-reinstall`
- Frontend: Clean install with `rm -rf node_modules package-lock.json && npm install`
- Auth: Install Better Auth packages separately if needed

## Next Steps

1. Generate implementation tasks: `/sp.tasks`
2. Begin implementation following agentic dev stack workflow
3. Implement backend authentication middleware using JWT
4. Integrate Better Auth with frontend Next.js application
5. Update existing task endpoints to require authentication
6. Test complete authentication flow (register → login → protected endpoints → logout)