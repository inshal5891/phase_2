#!/bin/bash

echo "Starting Todo Web Application development servers..."

# Start backend in the background
echo "Starting backend server..."
cd backend
source venv/bin/activate 2>/dev/null || true
uvicorn src.main:app --reload &
BACKEND_PID=$!

# Give backend a moment to start
sleep 2

# Start frontend in the background
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Set up cleanup function
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap to handle Ctrl+C
trap cleanup INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID