@echo off
echo ========================================
echo Multi-Agent AI System - Clean Installation
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Setting up Frontend...
cd ..\frontend
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Environment Setup...
cd ..\backend
if not exist .env (
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your API keys:
    echo - OPENAI_API_KEY=your_openai_api_key_here
    echo - NEWS_API_KEY=your_news_api_key_here
    echo.
)

echo.
echo [4/4] Verification...
echo Checking Python installation...
python --version
echo Checking Node.js installation...
cd ..\frontend
node --version
npm --version

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the system:
echo 1. Backend: cd backend && python main.py
echo 2. Frontend: cd frontend && npm run dev
echo.
echo Don't forget to add your API keys to backend\.env
echo.
pause
