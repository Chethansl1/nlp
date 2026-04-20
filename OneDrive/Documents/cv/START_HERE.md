
# Start Here - Lane Detection Application

## 🚀 EASIEST WAY (Recommended)

### First Time Only:
```
Double-click: setup_and_run.bat
```

**Wait 3-5 minutes** for setup to complete. You'll see:
1. Downloading npm packages
2. Setting up Python
3. Both services starting
4. Browser opening

### Every Time After:
```
Double-click: quick_start.bat
```

**Takes ~20 seconds** to start both services.

---

## If Services Don't Open Automatically

### Plan B: Manual Startup (Two Windows)

#### Window 1 - Frontend:
```
Double-click: run_frontend.bat
```
Wait for: "compiled successfully"

#### Window 2 - Backend:
```
Double-click: backend\run_backend.bat
```
Wait for: "Running on http://localhost:5000"

#### Then:
Open browser manually: `http://localhost:3000`

---

## If Batch Files Don't Work

### Plan C: Command Line (Manual)

#### Terminal 1 - Frontend:
```bash
npm install
npm start
```

#### Terminal 2 - Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

---

## Troubleshooting

### 1. Check What's Wrong:
```
Double-click: diagnose.bat
```
This shows what's missing and needs to be fixed.

### 2. Common Issues:

**"Node.js not found"**
- Download: https://nodejs.org/
- Install LTS version
- Restart computer

**"Python not found"**
- Download: https://python.org/
- **CHECK**: "Add Python to PATH" during install
- Restart computer

**"Port already in use"**
- Run: `diagnose.bat`
- Follow the kill process instructions

**"npm install fails"**
- Run: `npm cache clean --force`
- Then: `setup_and_run.bat` again

**"ModuleNotFoundError: No module named 'flask'"**
- Run: `backend\run_backend.bat`
- Should automatically install packages

---

## What You Should See

### ✅ Success Indicators:

**Browser shows:**
- Title: "🚗 Autonomous Vehicle Lane Detection"
- Header with status: "✅ Backend Connected" or "📡 Using Browser Processing"
- Upload button visible
- Can upload images

**React Terminal shows:**
- `compiled successfully`
- `Compiled with warnings` is OK

**Flask Terminal shows:**
- `Running on http://localhost:5000`
- `Method = POST`
- `/process` endpoint called

### ❌ If You See:

**Browser shows:**
- Blank page
- Error message
- Cannot connect

→ Check that both terminals are running without errors

---

## Using the App

1. **Open**: `http://localhost:3000`
2. **Upload**: Click "📷 Upload Image" button
3. **Choose** detection method:
   - Gradient (fastest ⚡)
   - Sobel (balanced)
   - Canny (best quality 🔥)
4. **Options**:
   - ✓ Show Gradient Magnitude
   - ✓ Highlight Lane Markings
5. **Click**: "Process Image"
6. **View**: Results in tabs (Original/Gradient/Sobel/Canny)

---

## File Guide

| File | Purpose | When to Use |
|------|---------|-----------|
| `setup_and_run.bat` | Complete setup + run | First time |
| `quick_start.bat` | Just run (no setup) | Every time after |
| `diagnose.bat` | Check what's wrong | Troubleshooting |
| `run_frontend.bat` | React app only | Manual startup |
| `backend\run_backend.bat` | Flask server only | Manual startup |

---

## Important Notes

⚠️ **First Time:**
- Takes 2-3 minutes to download npm packages
- ~200MB download
- Needs internet connection
- Don't close windows during setup

⚠️ **Python Environment:**
- Always activate venv before running backend
- Run `backend\run_backend.bat` NOT `python backend\app.py`

⚠️ **Ports:**
- Frontend uses port 3000
- Backend uses port 5000
- Make sure these ports are free
- Firewalls might block them

---

## Still Not Working?

### Step 1: Run Diagnostic
```
Double-click: diagnose.bat
```

### Step 2: Check for Errors
- Look for RED error messages
- Note the exact error text

### Step 3: Follow Guide
- See if error matches anything in this file
- Check: WINDOWS_SETUP.md
- Check: TROUBLESHOOTING.md

### Step 4: Manual Test
```bash
# Test if Node.js works
node --version

# Test if Python works
python --version

# Test if npm works
npm --version

# Test if ports are free
netstat -ano | findstr :3000
netstat -ano | findstr :5000
```

---

## Quick Reference

```bash
# First time
setup_and_run.bat

# Normal start
quick_start.bat

# Check issues
diagnose.bat

# Start separately
run_frontend.bat          (in one terminal)
backend\run_backend.bat   (in another terminal)

# Kill stuck services
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# Check if ports are free
netstat -ano | findstr :3000
netstat -ano | findstr :5000
```

---

## Folder Structure

```
cv/
├── setup_and_run.bat          ← Start here (first time)
├── quick_start.bat            ← Start here (after setup)
├── diagnose.bat               ← Check what's wrong
├── run_frontend.bat           ← React only
├── START_HERE.md              ← This file
├── WINDOWS_SETUP.md           ← Detailed setup
├── src/                       ← React code
├── backend/
│   ├── run_backend.bat        ← Flask only
│   ├── app.py                 ← Flask server
│   └── venv/                  ← Python environment
├── node_modules/              ← npm packages
└── public/
    └── index.html
```

---

## System Requirements

| Item | Need | Have |
|------|------|------|
| OS | Windows 7+ | ✓ |
| RAM | 4GB minimum | Check Task Mgr |
| Disk | 1GB free | Check C: drive |
| Node.js 16+ | Required | Run `node --version` |
| Python 3.8+ | Required | Run `python --version` |
| Internet | For setup | ✓ |

---

## Success Path

```
1. Run: setup_and_run.bat
   ↓
2. Wait for completion
   ↓
3. Browser opens to http://localhost:3000
   ↓
4. Upload image
   ↓
5. Choose method (Gradient/Sobel/Canny)
   ↓
6. Click "Process Image"
   ↓
7. See results!
   ↓
8. Read discussion points
```

---

## Next Time

Just run:
```
quick_start.bat
```

And you're good to go!

---

## Getting Help

### Documentation
- [README.md](README.md) - Full project info
- [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Windows-specific
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - How frontend/backend work
- [RUNNING.md](RUNNING.md) - How to use the app

### Quick Checks
```bash
diagnose.bat          # Check system status
```

---

## Let's Get Started! 🚗

### 👉 DO THIS NOW:

**First time?**
```
setup_and_run.bat
```

**Already set up?**
```
quick_start.bat
```

---

**That's it! The app will start automatically.**

If something doesn't work, run `diagnose.bat` 

If still stuck, see the documentation files.

**Good luck! 🚀**
