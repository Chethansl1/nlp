@echo off
cd /d "c:\Users\Admin\OneDrive\Documents\cv"

echo.
echo ======================================
echo Diagnostic Report
echo ======================================
echo.

echo [1/10] Checking Node.js...
where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js not installed
) else (
    node --version
)

echo.
echo [2/10] Checking Python...
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not installed
) else (
    python --version
)

echo.
echo [3/10] Checking npm packages...
if exist "node_modules" (
    echo OK: node_modules exists
    echo Package count: 
    dir /b node_modules | find /c "."
) else (
    echo ERROR: node_modules not found - run setup_and_run.bat
)

echo.
echo [4/10] Checking Python virtual environment...
if exist "backend\venv" (
    echo OK: Python venv exists
) else (
    echo ERROR: Python venv not found - run setup_and_run.bat
)

echo.
echo [5/10] Checking Python requirements...
if exist "backend\requirements.txt" (
    echo OK: requirements.txt found
    type backend\requirements.txt
) else (
    echo ERROR: requirements.txt not found
)

echo.
echo [6/10] Checking port 3000...
netstat -ano | findstr :3000 >nul 2>nul
if errorlevel 1 (
    echo OK: Port 3000 is free
) else (
    echo WARNING: Port 3000 is in use
    echo Current process:
    netstat -ano | findstr :3000
)

echo.
echo [7/10] Checking port 5000...
netstat -ano | findstr :5000 >nul 2>nul
if errorlevel 1 (
    echo OK: Port 5000 is free
) else (
    echo WARNING: Port 5000 is in use
    echo Current process:
    netstat -ano | findstr :5000
)

echo.
echo [8/10] Checking required files...
if exist "src\App.js" (
    echo OK: React App found
) else (
    echo ERROR: src\App.js not found
)

if exist "backend\app.py" (
    echo OK: Flask app found
) else (
    echo ERROR: backend\app.py not found
)

if exist "package.json" (
    echo OK: package.json found
) else (
    echo ERROR: package.json not found
)

echo.
echo [9/10] Checking .env file...
if exist ".env" (
    echo OK: .env file found
    type .env
) else (
    echo WARNING: .env not found - creating from example
    if exist ".env.example" (
        copy .env.example .env
        type .env
    )
)

echo.
echo [10/10] System Information...
echo Windows Version:
ver

echo.
echo ======================================
echo Diagnostic Complete
echo ======================================
echo.

if exist "node_modules" if exist "backend\venv" (
    echo You can run: quick_start.bat
) else (
    echo You need to run: setup_and_run.bat
)

echo.
pause
