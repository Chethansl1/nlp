@echo off

echo.
echo ======================================
echo Lane Detection App - Full Setup
echo ======================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if errorlevel 1 (
    echo X Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo X Python is not installed
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo OK Node.js version: %NODE_VERSION%

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo OK Python version: %PYTHON_VERSION%
echo.

REM Install npm dependencies if needed
if not exist "node_modules" (
    echo Downloading npm dependencies...
    call npm install
    if errorlevel 1 (
        echo X Failed to install npm dependencies
        pause
        exit /b 1
    )
    echo Installing concurrently...
    call npm install --save-dev concurrently
)

REM Create Python virtual environment if needed
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Activate virtual environment
call backend\venv\Scripts\activate.bat

REM Install Python dependencies
echo Downloading Python dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r backend\requirements.txt
if errorlevel 1 (
    echo X Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo ======================================
echo OK Setup Complete!
echo ======================================
echo.
echo Starting both frontend and backend...
echo Frontend will open at: http://localhost:3000
echo Backend API at: http://localhost:5000
echo.
echo Press Ctrl+C to stop both servers
echo ======================================
echo.

call npm run dev
pause
