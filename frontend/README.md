# Todo Web Application - Frontend

This is the frontend for the secure todo web application built with Next.js 16+ using the App Router.

## Features

- **Authentication**: Secure user registration and login with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **User Isolation**: Each user can only see and modify their own tasks
- **Responsive UI**: Mobile-friendly interface built with Tailwind CSS
- **Protected Routes**: Authentication required for accessing task management

## Architecture

### Components
- `AuthProvider`: Manages authentication state globally
- `ProtectedRoute`: Wrapper for pages requiring authentication
- `TaskForm`: Component for creating and editing tasks
- `TaskItem`: Individual task display with editing capability
- `TaskList`: Task list display with filtering options

### API Services
- `api/auth.ts`: Handles user registration, login, and logout
- `api/tasks.ts`: Handles all task-related API operations with JWT token management

### Context
- `AuthContext`: Provides authentication state and functions throughout the app

## Security Features

- JWT tokens stored securely in localStorage
- Automatic token inclusion in API requests
- Token expiration handling with automatic logout
- User data isolation - each user only accesses their own data
- Protected routes that redirect unauthenticated users

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API (defaults to http://localhost:8000/api)

## Getting Started

1. Install dependencies: `npm install`
2. Start the development server: `npm run dev`
3. Visit `http://localhost:3000` in your browser

The application will automatically redirect users based on their authentication status:
- Unauthenticated users → Login page
- Authenticated users → Tasks page