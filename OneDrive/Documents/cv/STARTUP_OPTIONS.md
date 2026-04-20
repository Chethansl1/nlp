# All Startup Options

Choose the method that works best for you.

## 🟢 Recommended: Automatic Setup (All-in-One)

### Files:
- `setup_and_run.bat` (First time only)
- `quick_start.bat` (Every time after)

### How:
1. **First time**: Double-click `setup_and_run.bat`
   - Installs everything
   - Starts both services
   - Opens browser

2. **Later times**: Double-click `quick_start.bat`
   - Just starts services
   - Much faster (~20 seconds)

### Pros:
- ✅ Easiest
- ✅ One click
- ✅ Handles everything automatically

### Cons:
- ⏱️ First time takes 2-3 minutes

---

## 🟡 Alternative: Separate Windows

### Files:
- `run_frontend.bat` (Terminal 1)
- `backend\run_backend.bat` (Terminal 2)

### How:
1. Open Terminal 1 and run: `run_frontend.bat`
2. Open Terminal 2 and run: `backend\run_backend.bat`
3. Open browser to: `http://localhost:3000`

### Pros:
- ✅ See each service separately
- ✅ Easy to debug
- ✅ Can restart one without other

### Cons:
- ⚠️ Need two windows
- ⚠️ Manual browser open

---

## 🔵 Manual: Command Line

### Windows Command Prompt:

**Terminal 1 - Frontend:**
```bash
npm install
npm start
```

**Terminal 2 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

### Mac/Linux Terminal:

**Terminal 1:**
```bash
npm install
npm start
```

**Terminal 2:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Pros:
- ✅ Most control
- ✅ See all output
- ✅ Can modify commands

### Cons:
- ⚠️ More typing
- ⚠️ Need to know commands
- ⚠️ Two terminals needed

---

## Diagnostic Tools

### Diagnose Issues:
```
diagnose.bat
```
Shows:
- ✓ Node.js version
- ✓ Python version
- ✓ Port status
- ✓ File status
- ✓ Recommendations

---

## Quick Comparison

| Method | Setup Time | Start Time | Difficulty | Use When |
|--------|-----------|-----------|-----------|----------|
| `setup_and_run.bat` | 2-3 min | 30 sec | ⭐ Very Easy | First time |
| `quick_start.bat` | - | 20 sec | ⭐ Very Easy | Normal start |
| Separate batch files | 1 min | 30 sec | ⭐⭐ Easy | Debugging |
| Command line | 1 min | 30 sec | ⭐⭐⭐ Medium | Advanced |

---

## Decision Tree

```
First time?
├─ YES → Run: setup_and_run.bat
│        (Waits 2-3 minutes for setup)
│
└─ NO → Use: quick_start.bat
        (Takes ~20 seconds)
        
Troubleshooting?
├─ YES → Run: diagnose.bat
│        (Shows what's wrong)
│
└─ NO → Continue as above

Not working?
├─ YES → Read: WINDOWS_SETUP.md or TROUBLESHOOTING.md
│
└─ NO → Great! Start using the app
```

---

## Troubleshooting by Symptom

### "Batch files won't open"
→ Use Command Line method

### "Only see one service starting"
→ Use Separate batch files method

### "Don't know what's wrong"
→ Run `diagnose.bat`

### "Want maximum control"
→ Use Command Line method

### "Just want it to work"
→ Use `quick_start.bat`

---

## File Locations

```
c:\Users\Admin\OneDrive\Documents\cv\
├── setup_and_run.bat           ← Run this first
├── quick_start.bat             ← Run this after setup
├── diagnose.bat                ← If something wrong
├── run_frontend.bat            ← React only
├── backend\
│   ├── run_backend.bat         ← Flask only
│   ├── app.py
│   ├── requirements.txt
│   └── venv\
│       └── Scripts\
│           ├── activate.bat
│           └── python.exe
├── src\
│   ├── App.js
│   └── components\
├── node_modules\
└── public\
    └── index.html
```

---

## What Each Does

### `setup_and_run.bat`
1. Checks Node.js and Python
2. Installs npm packages (~200MB)
3. Creates Python virtual environment
4. Installs Python packages
5. Starts React frontend on port 3000
6. Starts Flask backend on port 5000
7. Opens browser to localhost:3000

### `quick_start.bat`
1. Activates Python environment
2. Starts React frontend on port 3000
3. Starts Flask backend on port 5000

### `diagnose.bat`
1. Checks Node.js installation
2. Checks Python installation
3. Checks npm packages
4. Checks Python venv
5. Checks port availability
6. Checks required files
7. Shows recommendations

### `run_frontend.bat`
1. Checks Node.js
2. Starts React app on port 3000
3. Displays any errors

### `backend\run_backend.bat`
1. Activates Python environment
2. Starts Flask on port 5000
3. Displays any errors

---

## Success Checklist

After choosing a method:

- [ ] Both command windows open
- [ ] No RED error messages
- [ ] React shows "compiled successfully"
- [ ] Flask shows "Running on http://localhost:5000"
- [ ] Browser opens to http://localhost:3000
- [ ] Upload button visible
- [ ] Can upload images
- [ ] Can process images

---

## Services Running

### React Frontend (Port 3000)
- URL: `http://localhost:3000`
- Purpose: Web interface, image upload
- Technology: React 18, OpenCV.js
- Hot reload: Yes (auto-updates on code changes)

### Flask Backend (Port 5000)
- URL: `http://localhost:5000`
- Purpose: Image processing, API
- Technology: Flask, OpenCV, Python
- Auto-reload: No (restart needed after changes)

---

## Stopping Services

### Method 1: Close Windows
- Ctrl+C in each window

### Method 2: Kill Processes
```bash
taskkill /F /IM node.exe      # Kill all Node.js
taskkill /F /IM python.exe    # Kill all Python
```

### Method 3: Task Manager
- Find: node.exe (React)
- Find: python.exe (Flask)
- Right-click → End Task

---

## Next Run

After stopping services:

**Next time:**
```
quick_start.bat
```

**Or if using separate batch files:**
```
run_frontend.bat       (Window 1)
backend\run_backend.bat (Window 2)
```

---

## Recommendations

### For First Time Users:
→ `setup_and_run.bat` (All automatic)

### For Regular Use:
→ `quick_start.bat` (Fast startup)

### For Development:
→ Separate batch files or Command Line
(Better visibility, easier debugging)

### For Troubleshooting:
→ `diagnose.bat` (See what's wrong)

---

## Support

**Still stuck?** Read:
- [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Windows-specific guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [START_HERE.md](START_HERE.md) - Getting started

**Quick diagnostics:**
```
diagnose.bat
```

---

## TL;DR

```
First time?
→ setup_and_run.bat

Every time after?
→ quick_start.bat

Something wrong?
→ diagnose.bat

Need separate control?
→ run_frontend.bat + backend\run_backend.bat
```

**Pick one and start! 🚀**
