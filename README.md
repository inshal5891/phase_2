# Todo Web Application

A full-stack todo web application built with Next.js, FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Features

- Create, read, update, and delete todo tasks
- Filter tasks by completion status (all, completed, pending)
- Persistent storage in PostgreSQL database
- Responsive web interface
- RESTful API endpoints

## Tech Stack

- **Frontend**: Next.js 16+ (App Router), TypeScript, React
- **Backend**: FastAPI, Python 3.12
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **API**: REST with automatic OpenAPI documentation

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── models/          # SQLModel definitions
│   │   ├── services/        # Business logic
│   │   ├── api/            # API routes
│   │   ├── database/       # Database session management
│   │   └── main.py         # Main application entry point
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   ├── components/     # React components
│   │   └── api/           # API service functions
│   ├── package.json
│   ├── next.config.js
│   └── .env.local
├── shared/
│   └── types/             # Shared TypeScript definitions
└── specs/
    └── 001-fullstack-todo-app/  # Project specifications
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database connection string
```

5. Start the backend server:
```bash
cd src
uvicorn main:app --reload
```
The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local with your backend API URL
```

4. Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

The application exposes the following REST API endpoints:

- `GET /api/tasks` - Get all tasks for a user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

View the full API documentation at `http://localhost:8000/docs` when the backend is running.

## Development

- Backend API documentation is automatically generated at `/docs`
- Frontend uses TypeScript with shared type definitions
- All database operations use SQLModel for type safety
- Frontend communicates with backend via API service functions

## Acknowledgements

Built with Claude Code's agentic development workflow.