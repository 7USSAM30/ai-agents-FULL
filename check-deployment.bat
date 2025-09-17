@echo off
REM Multi-Agent AI System - Deployment Error Prevention Script for Windows
REM This script checks for common deployment issues before deployment

echo 🔍 Multi-Agent AI System - Deployment Check
echo ==========================================

REM Check if we're in the right directory
if not exist "package.json" (
    echo [❌] Please run this script from the project root directory
    exit /b 1
)

if not exist "frontend" (
    echo [❌] Frontend directory not found
    exit /b 1
)

if not exist "backend" (
    echo [❌] Backend directory not found
    exit /b 1
)

echo [ℹ️] Checking project structure...

REM Check backend structure
echo [ℹ️] Checking backend structure...
if exist "backend\Procfile" (
    echo [✅] Procfile exists
) else (
    echo [❌] Procfile missing in backend/
    exit /b 1
)

if exist "backend\requirements.txt" (
    echo [✅] requirements.txt exists
) else (
    echo [❌] requirements.txt missing in backend/
    exit /b 1
)

if exist "backend\runtime.txt" (
    echo [✅] runtime.txt exists
) else (
    echo [❌] runtime.txt missing in backend/
    exit /b 1
)

if exist "backend\start.py" (
    echo [✅] start.py exists
) else (
    echo [❌] start.py missing in backend/
    exit /b 1
)

if exist "backend\main.py" (
    echo [✅] main.py exists
) else (
    echo [❌] main.py missing in backend/
    exit /b 1
)

REM Check frontend structure
echo [ℹ️] Checking frontend structure...
if exist "frontend\package.json" (
    echo [✅] package.json exists
) else (
    echo [❌] package.json missing in frontend/
    exit /b 1
)

if exist "frontend\next.config.js" (
    echo [✅] next.config.js exists
) else (
    echo [❌] next.config.js missing in frontend/
    exit /b 1
)

if exist "frontend\vercel.json" (
    echo [✅] vercel.json exists
) else (
    echo [❌] vercel.json missing in frontend/
    exit /b 1
)

if exist "frontend\src\lib\api.ts" (
    echo [✅] API client exists
) else (
    echo [❌] API client missing in frontend/src/lib/
    exit /b 1
)

REM Check Procfile content
echo [ℹ️] Checking Procfile content...
findstr /C:"python start.py" backend\Procfile >nul
if errorlevel 1 (
    echo [❌] Procfile has incorrect start command
    echo [ℹ️] Expected: web: python start.py
) else (
    echo [✅] Procfile has correct start command
)

REM Check requirements.txt for pinned versions
echo [ℹ️] Checking requirements.txt...
findstr /C:"==" backend\requirements.txt >nul
if errorlevel 1 (
    echo [⚠️] requirements.txt should use pinned versions (==) for production
) else (
    echo [✅] requirements.txt uses pinned versions
)

REM Check runtime.txt
echo [ℹ️] Checking runtime.txt...
findstr /C:"python-3.11.9" backend\runtime.txt >nul
if errorlevel 1 (
    echo [⚠️] Python version in runtime.txt may not be optimal
    echo [ℹ️] Recommended: python-3.11.9
) else (
    echo [✅] Correct Python version specified
)

REM Check environment files
echo [ℹ️] Checking environment configuration...
if exist "frontend\.env.local.example" (
    echo [✅] Environment example file exists
) else (
    echo [⚠️] No .env.local.example file found
)

REM Check for API routes in frontend (should be removed)
echo [ℹ️] Checking for removed API routes...
if exist "frontend\src\app\api" (
    echo [❌] API routes still exist in frontend - they should be removed
    echo [ℹ️] Run: rmdir /s /q frontend\src\app\api
) else (
    echo [✅] API routes properly removed from frontend
)

REM Check CORS configuration
echo [ℹ️] Checking CORS configuration...
findstr /C:"vercel.app" backend\main.py >nul
if errorlevel 1 (
    echo [⚠️] CORS may not be configured for Vercel domains
) else (
    echo [✅] CORS configured for Vercel domains
)

REM Check for common Python issues
echo [ℹ️] Checking Python configuration...
findstr /C:"import.*agents" backend\main.py >nul
if errorlevel 1 (
    echo [❌] Agent imports not found in main.py
) else (
    echo [✅] Agent imports found
)

REM Check for error handling
echo [ℹ️] Checking error handling...
findstr /C:"try:" backend\main.py >nul
if errorlevel 1 (
    echo [⚠️] Consider adding error handling to main.py
) else (
    echo [✅] Error handling implemented
)

REM Check Next.js configuration
echo [ℹ️] Checking Next.js configuration...
findstr /C:"NEXT_PUBLIC_API_BASE_URL" frontend\next.config.js >nul
if errorlevel 1 (
    echo [⚠️] API base URL not configured in Next.js
) else (
    echo [✅] API base URL configured in Next.js
)

REM Check API client configuration
echo [ℹ️] Checking API client...
findstr /C:"process.env.NEXT_PUBLIC_API_BASE_URL" frontend\src\lib\api.ts >nul
if errorlevel 1 (
    echo [❌] API client not using environment variables
) else (
    echo [✅] API client uses environment variables
)

REM Summary
echo.
echo [ℹ️] Deployment check completed!
echo.
echo [ℹ️] Next steps:
echo 1. Set environment variables in Railway dashboard
echo 2. Set environment variables in Vercel dashboard
echo 3. Deploy backend to Railway
echo 4. Deploy frontend to Vercel
echo 5. Test the integration
echo.
echo [ℹ️] For detailed instructions, see DEPLOYMENT_CHECKLIST.md
