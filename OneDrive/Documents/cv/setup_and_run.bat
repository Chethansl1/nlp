@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\Admin\OneDrive\Documents\cv"

echo.
echo ======================================
echo Lane Detection - Complete Setup
echo ======================================
echo.

REM Check Node.js
echo Checking Node.js...
where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js not found
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do echo Node.js: %%i
)

REM Check Python
echo Checking Python...
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found
    echo Download from: https://python.org/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do echo Python: %%i
)

echo.
echo ======================================
echo Installing Dependencies...
echo ======================================
echo.

REM Install npm dependencies
if not exist "node_modules" (
    echo Installing npm packages... (this may take 2-3 minutes)
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed
        pause
        exit /b 1
    )
) else (
    echo npm packages already installed
)

REM Install concurrently
echo Installing concurrently...
call npm install --save-dev concurrently >nul 2>&1

REM Check and set up Python venv
echo.
echo Setting up Python environment...
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Activate venv and install Python packages
echo Activating Python virtual environment...
call backend\venv\Scripts\activate.bat

echo Installing Python packages...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r backend\requirements.txt
if errorlevel 1 (
    echo WARNING: Some Python packages failed to install
    echo Continuing anyway...
)

echo.
echo ======================================
echo Setup Complete! Starting Services...
echo ======================================
echo.

REM Create a startup wrapper
echo Starting React Frontend... (port 3000)
echo Starting Flask Backend... (port 5000)
echo.
echo Browser will open automatically...
echo Press Ctrl+C to stop both services
echo.

timeout /t 3

REM Run with concurrently
call npm run dev

pause
