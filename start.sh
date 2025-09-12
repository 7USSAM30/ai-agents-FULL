#!/bin/sh

# Multi-Agent AI System - Unified Startup Script
# This script starts both the FastAPI backend and Next.js frontend

echo "🚀 Starting Multi-Agent AI System..."

# Function to handle cleanup on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start FastAPI backend in background
echo "🔧 Starting FastAPI backend on port 8000..."
cd /app/backend
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend started successfully (PID: $BACKEND_PID)"

# Start Next.js frontend
echo "🎨 Starting Next.js frontend on port 3000..."
cd /app/frontend
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"
echo "🌐 Application is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
