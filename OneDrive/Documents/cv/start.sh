#!/bin/bash

echo ""
echo "======================================"
echo "Lane Detection App - Full Setup"
echo "======================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    echo "Please install Python from https://python.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python version: $(python3 --version 2>/dev/null || python --version)"
echo ""

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install npm dependencies"
        exit 1
    fi
    npm install --save-dev concurrently
fi

# Create Python virtual environment if needed
if [ ! -d "backend/venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv || python -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source backend/venv/Scripts/activate
else
    # macOS/Linux
    source backend/venv/bin/activate
fi

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Starting both frontend and backend..."
echo "Frontend will open at: http://localhost:3000"
echo "Backend API at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "======================================"
echo ""

npm run dev
