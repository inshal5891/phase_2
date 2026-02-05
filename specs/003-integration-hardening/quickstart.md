# Quickstart Guide: Integration, Hardening & Production Readiness

## Overview
Quick setup guide for the authenticated full-stack todo application with integration and hardening features.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.12+ (for backend)
- npm/yarn (for frontend dependencies)
- pip (for backend dependencies)
- Neon Serverless PostgreSQL database instance

## Environment Setup

### Backend Configuration
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   DATABASE_URL=your_neon_database_url
   SECRET_KEY=your_jwt_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Start the backend server:
   ```
   uvicorn src.main:app --reload
   ```

### Frontend Configuration
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the frontend development server:
   ```
   npm run dev
   ```

## Application Flow

### 1. End-to-End User Flow
1. Visit the application homepage
2. Navigate to sign-up page to create an account
3. Log in with your credentials
4. Create, view, update, and delete tasks
5. Log out when finished

### 2. API Testing
- API endpoints accessible at `http://localhost:8000/api`
- Frontend communicates with backend via HTTP requests
- JWT tokens automatically included in requests after login

## Integration Points

### Frontend-Backend Communication
- Frontend makes API calls to backend with JWT tokens
- Authentication state managed via React Context
- Error handling implemented for network issues

### Authentication Flow
- User registers via `/api/auth/register`
- User authenticates via `/api/auth/login`
- JWT token stored in localStorage
- Token included in all protected API requests

### Data Isolation
- Each user's tasks are isolated from others
- Backend validates user ownership on each request
- Database queries filtered by authenticated user ID

## Testing the Hardened Features

### 1. Authentication Validation
- Attempt to access protected routes without login
- Verify 401 responses for invalid/missing tokens
- Test JWT token expiration handling

### 2. Data Isolation
- Create multiple user accounts
- Verify users only see their own tasks
- Attempt to access other users' tasks and confirm 404 responses

### 3. Error Handling
- Submit invalid credentials during login
- Test API endpoints with invalid JWT tokens
- Verify appropriate error messages are displayed

## Common Issues and Solutions

### 1. Environment Variables Not Loaded
- Ensure `.env` files are properly configured
- Restart servers after changing environment variables

### 2. Database Connection Issues
- Verify database URL is correct
- Ensure database instance is running and accessible

### 3. Authentication Problems
- Clear browser storage if authentication issues persist
- Verify JWT secret key is the same in frontend and backend

## Next Steps
1. Review the API documentation at `/docs` endpoint
2. Test all user flows to ensure proper integration
3. Verify all security measures are functioning as expected
4. Prepare for demo by testing end-to-end flows