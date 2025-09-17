@echo off
REM Multi-Agent AI System - Separated Deployment Script for Windows
REM This script helps deploy frontend to Vercel and backend to Railway

echo 🚀 Multi-Agent AI System - Separated Deployment
echo ==============================================

REM Check if we're in the right directory
if not exist "package.json" (
    echo [ERROR] Please run this script from the project root directory
    exit /b 1
)

if not exist "frontend" (
    echo [ERROR] Frontend directory not found!
    exit /b 1
)

if not exist "backend" (
    echo [ERROR] Backend directory not found!
    exit /b 1
)

REM Function to deploy backend to Railway
:deploy_backend
echo [STEP] Deploying Backend to Railway...

cd backend

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Railway CLI not found. Installing...
    npm install -g @railway/cli
)

REM Check if user is logged in
railway whoami >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Please login to Railway first:
    echo railway login
    exit /b 1
)

echo [INFO] Deploying to Railway...
railway up

echo [INFO] ✅ Backend deployed to Railway!
echo [WARNING] Don't forget to set environment variables in Railway dashboard:
echo   - NEWS_API_KEY
echo   - OPENAI_API_KEY
echo   - WEAVIATE_URL
echo   - WEAVIATE_API_KEY

cd ..

goto :eof

REM Function to deploy frontend to Vercel
:deploy_frontend
echo [STEP] Deploying Frontend to Vercel...

cd frontend

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if user is logged in
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Please login to Vercel first:
    echo vercel login
    exit /b 1
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo [WARNING] .env.local not found. Creating from example...
    copy .env.local.example .env.local
    echo [WARNING] Please edit .env.local with your Railway backend URL!
    echo NEXT_PUBLIC_API_BASE_URL=https://your-railway-app.railway.app
)

echo [INFO] Deploying to Vercel...
vercel --prod

echo [INFO] ✅ Frontend deployed to Vercel!

cd ..

goto :eof

REM Main script logic
if "%1"=="backend" (
    call :deploy_backend
) else if "%1"=="frontend" (
    call :deploy_frontend
) else if "%1"=="help" (
    echo Usage: %0 [OPTION]
    echo.
    echo Options:
    echo   backend    Deploy only the backend to Railway
    echo   frontend   Deploy only the frontend to Vercel
    echo   all        Deploy both backend and frontend (default)
    echo   help       Show this help message
    echo.
    echo Examples:
    echo   %0 backend    # Deploy only backend
    echo   %0 frontend   # Deploy only frontend
    echo   %0 all        # Deploy both (default)
) else (
    call :deploy_backend
    echo.
    call :deploy_frontend
)

echo.
echo [INFO] 🎉 Deployment completed!
echo.
echo [WARNING] Next steps:
echo 1. Set environment variables in Railway dashboard
echo 2. Update NEXT_PUBLIC_API_BASE_URL in Vercel with your Railway URL
echo 3. Test the integration between frontend and backend
echo.
echo [INFO] Check DEPLOYMENT_SEPARATED.md for detailed instructions
