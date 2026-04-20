@echo off
cd /d "%~dp0"

echo.
echo ======================================
echo Lane Detection - Flask Backend
echo ======================================
echo.

REM Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found
    echo Download from: https://python.org/
    pause
    exit /b 1
)

echo Python found: 
python --version

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Flask server...
echo Backend will be available at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py

pause
