#!/bin/bash

# Start development environment
echo "Starting Economic Indicators Dashboard..."

# Start backend
echo "Starting backend server..."
cd backend
source .venv/bin/activate
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend running on http://127.0.0.1:8000"
echo "Frontend running on http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
