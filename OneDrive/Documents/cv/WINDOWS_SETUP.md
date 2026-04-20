# Windows Setup Guide

Complete step-by-step guide to get the Lane Detection app running on Windows.

## Step 1: Check Your System

First, run the diagnostic tool:

```bash
diagnose.bat
```

This will check:
- ✓ Node.js installation
- ✓ Python installation
- ✓ npm packages
- ✓ Port availability
- ✓ Required files

---

## Step 2: Initial Setup (First Time Only)

Double-click this file:
```
setup_and_run.bat
```

**What it does:**
1. Checks Node.js and Python
2. Installs npm dependencies (~200MB, takes 2-3 minutes)
3. Creates Python virtual environment
4. Installs Python packages
5. Starts both services automatically

**You'll see:**
```
Installing npm packages... (this may take 2-3 minutes)
Setting up Python environment...
Starting React Frontend... (port 3000)
Starting Flask Backend... (port 5000)
```

**Wait for both to start**, then:
- Browser should open automatically
- If not, open `http://localhost:3000` manually

---

## Step 3: On Subsequent Runs

After first setup, just run:
```
quick_start.bat
```

This skips setup and starts both services immediately.

---

## Troubleshooting

### Issue 1: Services won't start

**Solution:**
1. Run `diagnose.bat` to check what's wrong
2. Look for ERROR messages
3. Follow solutions below

### Issue 2: "Node.js not found"

**Solution:**
1. Download from https://nodejs.org/
2. Install the LTS version
3. Restart your computer
4. Run `diagnose.bat` again

### Issue 3: "Python not found"

**Solution:**
1. Download from https://python.org/
2. **IMPORTANT**: Check "Add Python to PATH" during install
3. Restart your computer
4. Run `diagnose.bat` again

### Issue 4: Port 3000 already in use

**Solution:**
```bash
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace XXXX with PID from above)
taskkill /PID XXXX /F

# Then try again
quick_start.bat
```

### Issue 5: Port 5000 already in use

**Solution:**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace XXXX with PID from above)
taskkill /PID XXXX /F

# Then try again
quick_start.bat
```

### Issue 6: npm install fails

**Solution:**
```bash
# Option 1: Clear npm cache
npm cache clean --force
setup_and_run.bat

# Option 2: If that fails, delete node_modules and try again
rmdir /s /q node_modules
setup_and_run.bat
```

### Issue 7: "Microsoft Visual C++ is required"

**Solution:**
1. Download Microsoft Visual C++ Build Tools:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install it
3. Restart computer
4. Run `setup_and_run.bat` again

### Issue 8: Browser won't open to localhost:3000

**Solution:**
1. Make sure services started (check command window)
2. Manually open: http://localhost:3000
3. If still fails, check if port 3000 is available:
   ```bash
   diagnose.bat
   ```

### Issue 9: Backend not connecting (shows "📡 Using Browser Processing")

**Solution:**
1. Check if port 5000 is running:
   ```bash
   netstat -ano | findstr :5000
   ```
2. If not found, Flask didn't start
3. Check command window for error messages
4. Run `diagnose.bat`

### Issue 10: Cannot activate Python environment

**Solution:**
1. Make sure Python is in PATH:
   ```bash
   python --version
   ```
2. Recreate venv:
   ```bash
   rmdir /s /q backend\venv
   python -m venv backend\venv
   backend\venv\Scripts\activate.bat
   pip install -r backend\requirements.txt
   ```

---

## Manual Startup (If Batch Files Don't Work)

### Terminal 1: Frontend

```bash
cd "c:\Users\Admin\OneDrive\Documents\cv"
npm start
```

Wait for it to say "compiled successfully" then move to Terminal 2.

### Terminal 2: Backend

```bash
cd "c:\Users\Admin\OneDrive\Documents\cv"
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

Then open browser to: http://localhost:3000

---

## Advanced Troubleshooting

### Check if npm is working
```bash
npm --version
npm list
```

### Check if Python is working
```bash
python --version
python -c "import cv2; print(cv2.__version__)"
```

### Check if ports are open
```bash
# Port 3000
netstat -ano | findstr :3000

# Port 5000
netstat -ano | findstr :5000
```

### Kill all Node processes
```bash
taskkill /F /IM node.exe
```

### Kill all Python processes
```bash
taskkill /F /IM python.exe
```

---

## System Requirements

| Item | Minimum | Recommended |
|------|---------|------------|
| RAM | 4GB | 8GB+ |
| Disk | 1GB free | 5GB free |
| Windows | 7 SP1 | 10/11 |
| Node.js | 16.x | 18.x LTS |
| Python | 3.8 | 3.9+ |

---

## Files Explained

| File | Purpose |
|------|---------|
| `setup_and_run.bat` | First time: Complete setup + run |
| `quick_start.bat` | Subsequent times: Just run services |
| `diagnose.bat` | Check what's wrong |

---

## Environment Variables

If you need to customize:

1. Create or edit `.env` file:
```
REACT_APP_API_URL=http://localhost:5000
FLASK_ENV=development
FLASK_DEBUG=False
```

2. Save and restart services

---

## Getting Help

1. Run: `diagnose.bat` (saves report)
2. Look for ERROR messages
3. Check this guide for that error
4. Still stuck? Check full docs:
   - [README.md](README.md)
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

---

## Fresh Install (Nuclear Option)

If everything is broken:

```bash
REM Delete everything
rmdir /s /q node_modules
rmdir /s /q backend\venv
del package-lock.json

REM Start fresh
setup_and_run.bat
```

---

## Success Indicators

When everything is working, you should see:

**Terminal output:**
```
> react-scripts start
webpack compiled successfully

On Your Network: http://192.168.x.x:3000
Local: http://localhost:3000/
```

And:
```
🚀 Lane Detection Backend Server
Running on http://localhost:5000
```

**Browser:**
- Page loads at http://localhost:3000
- Header shows "✅ Backend Connected"
- Upload button visible and clickable

---

## Quick Reference

```bash
# First time
setup_and_run.bat

# Later runs
quick_start.bat

# Check what's wrong
diagnose.bat

# Manual frontend
npm start

# Manual backend
cd backend
python app.py

# Kill stuck services
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

---

## Next Steps

1. Run `setup_and_run.bat`
2. Wait for both services to start
3. Browser opens to http://localhost:3000
4. Upload an image
5. Choose detection method
6. Click "Process Image"
7. View results!

---

**Need help?** Run `diagnose.bat` to see what's happening.

**Ready?** Double-click `setup_and_run.bat` to get started! 🚀
