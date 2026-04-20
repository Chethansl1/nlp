@echo off
cd /d "%~dp0"

echo.
echo ======================================
echo Lane Detection - React Frontend
echo ======================================
echo.

REM Check Node.js
where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js not found
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js found:
node --version

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo Press Ctrl+C to stop
echo.

call npm start

pause
