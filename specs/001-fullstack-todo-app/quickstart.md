# Quickstart Guide: Core Full-Stack Todo Web Application

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.12+ for backend development
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Git for version control
- Access to Claude Code agents (frontend, backend, database, auth)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
git checkout 001-fullstack-todo-app  # Use the feature branch
```

### 2. Backend Setup (FastAPI + SQLModel + Neon PostgreSQL)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# If requirements.txt doesn't exist yet, install the base dependencies:
pip install fastapi uvicorn sqlmodel psycopg[binary] python-dotenv python-jose[cryptography] passlib[bcrypt] pytest httpx

# Set up environment variables
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string:
# DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 3. Frontend Setup (Next.js 16+ App Router)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.local.example .env.local
# Configure API endpoints:
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

### 4. Database Initialization

```bash
# From backend directory
cd src

# Initialize the database tables
python -c "
from backend.database.session import engine
from backend.models import task
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(engine)
print('Database tables created successfully')
"
```

Alternatively, use alembic for migrations:

```bash
# Initialize alembic (first time only)
alembic init alembic

# Generate migration from models
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Running the Application

### 1. Start Backend Server

```bash
# From backend directory
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 2. Start Frontend Server

```bash
# From frontend directory
cd frontend
npm run dev
# or
yarn dev
```

Frontend will be available at `http://localhost:3000`

## API Endpoints

Once running, the following endpoints will be available:

```
GET    /api/tasks          # Get all tasks
POST   /api/tasks          # Create new task
GET    /api/tasks/{id}     # Get specific task
PUT    /api/tasks/{id}     # Update entire task
DELETE /api/tasks/{id}     # Delete task
PATCH  /api/tasks/{id}/complete  # Toggle completion status
```

## Development Workflow

1. **Architecture Decisions**: Document any significant changes in Architecture Decision Records (ADRs)
2. **Task Creation**: Use `/sp.tasks` to generate implementation tasks from the plan
3. **Agent Utilization**:
   - Use `nextjs-ui-optimizer` for frontend components
   - Use `fastapi-backend-engineer` for API endpoints
   - Use `neon-db-manager` for database schema
   - Use `auth-security-specialist` for authentication features (Spec 2)
4. **Testing**: Run tests after each major implementation:
   ```bash
   # Backend tests
   pytest tests/

   # Frontend tests
   npm run test
   ```

## Common Commands

```bash
# Generate tasks from plan
/sp.tasks

# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm run test

# Check backend API docs
http://localhost:8000/docs

# Format code
cd backend && black src/
cd frontend && npm run format
```

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` in environment variables
- Ensure Neon PostgreSQL is active and accessible
- Check firewall rules if running remotely

### Frontend Cannot Reach Backend
- Verify `NEXT_PUBLIC_API_BASE_URL` is correctly set
- Check CORS settings in FastAPI backend
- Ensure both servers are running simultaneously

### Dependency Issues
- Backend: Reinstall with `pip install -r requirements.txt --force-reinstall`
- Frontend: Clean install with `rm -rf node_modules package-lock.json && npm install`

## Next Steps

1. Generate implementation tasks: `/sp.tasks`
2. Begin implementation following agentic dev stack workflow
3. Create API contracts in `shared/contracts/`
4. Implement backend services using FastAPI and SQLModel
5. Build frontend components using Next.js App Router
6. Connect frontend to backend APIs
7. Test full CRUD functionality