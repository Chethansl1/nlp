@echo off
cd /d "c:\Users\Admin\OneDrive\Documents\cv"

echo.
echo ======================================
echo Lane Detection - Quick Start
echo ======================================
echo.

REM Activate Python venv
if not exist "backend\venv" (
    echo ERROR: Python environment not set up
    echo Run setup_and_run.bat first
    pause
    exit /b 1
)

echo Activating Python environment...
call backend\venv\Scripts\activate.bat

echo.
echo Starting both services:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

timeout /t 2

REM Run both services
npm run dev

pause
