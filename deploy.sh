#!/bin/bash

# Multi-Agent AI System - Unified Deployment Script
# This script handles deployment to Vercel with cleanup of old projects

set -e

echo "🚀 Multi-Agent AI System - Unified Deployment"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_error "Vercel CLI is not installed. Please install it first:"
    echo "npm install -g vercel"
    exit 1
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    print_warning "Not logged in to Vercel. Please login first:"
    vercel login
fi

print_step "1. Checking for old projects..."

# List existing Vercel projects
print_status "Current Vercel projects:"
vercel ls

# Ask about old project cleanup
echo ""
read -p "Do you want to remove the old 'ai-agent-full' project? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "2. Removing old project..."
    
    # Try to remove the old project
    if vercel remove ai-agent-full --yes 2>/dev/null; then
        print_status "✅ Old project 'ai-agent-full' removed successfully"
    else
        print_warning "⚠️  Could not remove 'ai-agent-full' (may not exist or already removed)"
    fi
else
    print_status "Skipping old project removal"
fi

print_step "3. Preparing environment variables..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.production.example .env
    print_warning "⚠️  Please edit .env file with your actual API keys before deploying!"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

print_step "4. Building and testing locally..."

# Build the Docker image locally first
print_status "Building Docker image..."
if docker build -t multi-agent-ai-unified .; then
    print_status "✅ Docker image built successfully"
else
    print_error "❌ Docker build failed!"
    exit 1
fi

print_step "5. Deploying to Vercel..."

# Deploy to Vercel
print_status "Deploying unified application to Vercel..."
if vercel --prod --docker; then
    print_status "✅ Deployment successful!"
else
    print_error "❌ Deployment failed!"
    exit 1
fi

print_step "6. Setting up environment variables in Vercel..."

# Set environment variables in Vercel
print_status "Setting environment variables..."

# Read .env file and set variables in Vercel
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ ! $key =~ ^# ]] && [[ -n $key ]]; then
        # Remove quotes from value if present
        value=$(echo "$value" | sed 's/^"//;s/"$//')
        print_status "Setting $key..."
        vercel env add "$key" production <<< "$value" 2>/dev/null || true
    fi
done < .env

print_status "🎉 Deployment completed successfully!"
print_status ""
print_status "Your unified Multi-Agent AI System is now deployed!"
print_status "Access it at: https://$(vercel ls --json | jq -r '.[0].url')"
print_status ""
print_status "Features:"
print_status "  ✅ Single unified application"
print_status "  ✅ Next.js frontend with integrated API routes"
print_status "  ✅ All AI agents running in one container"
print_status "  ✅ Optimized for Vercel deployment"
print_status ""
print_status "API Endpoints:"
print_status "  /api/query - Main query processing"
print_status "  /api/health - Health check"
print_status "  /api/agents/status - Agent status"
