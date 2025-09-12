#!/bin/bash

# Multi-Agent AI System - Unified Build Script
# This script builds and tests the unified Next.js application

set -e

echo "🚀 Building Unified Multi-Agent AI System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.production.example .env
    print_warning "Please edit .env file with your actual API keys before running the container."
fi

# Build the Docker image
print_status "Building Docker image..."
docker build -t multi-agent-ai:latest .

if [ $? -eq 0 ]; then
    print_status "✅ Docker image built successfully!"
else
    print_error "❌ Docker build failed!"
    exit 1
fi

# Test the image
print_status "Testing Docker image..."
docker run --rm -d --name test-container -p 3000:3000 -p 8000:8000 multi-agent-ai:latest

# Wait for services to start
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
    print_status "✅ Frontend is running on http://localhost:3000"
else
    print_warning "⚠️  Frontend health check failed"
fi

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Backend is running on http://localhost:8000"
else
    print_warning "⚠️  Backend health check failed"
fi

# Stop test container
docker stop test-container

print_status "🎉 Build completed successfully!"
print_status "To run the application:"
print_status "  docker run -p 3000:3000 -p 8000:8000 --env-file .env multi-agent-ai:latest"
print_status "Or use docker-compose:"
print_status "  docker-compose up --build"
