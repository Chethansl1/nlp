# Frontend & Backend Integration Guide

This guide explains how to run the frontend and backend together as one complete application.

## Quick Start (One Command)

### Windows
```bash
start.bat
```

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

**This single command will:**
1. ✅ Check dependencies (Node.js and Python)
2. ✅ Install npm packages
3. ✅ Create Python virtual environment
4. ✅ Install Python dependencies
5. ✅ Start React frontend on port 3000
6. ✅ Start Flask backend on port 5000
7. ✅ Automatically connect both services

---

## Manual Setup

### Option 1: Separate Terminals (More Control)

**Terminal 1 - Frontend:**
```bash
npm install
npm start
```
- Opens at `http://localhost:3000`
- Auto-reloads on code changes

**Terminal 2 - Backend:**
```bash
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run backend
python app.py
```
- Runs on `http://localhost:5000`

### Option 2: Single Terminal (Parallel)

```bash
# Install concurrently once
npm install --save-dev concurrently

# Set up Python (one time)
cd backend
python -m venv venv
# Activate venv and install requirements

# Then run:
npm run dev
```

---

## How They Work Together

### Architecture Flow

```
┌─────────────────────────────────────────┐
│     React Frontend (Port 3000)          │
│  • Image Upload Interface               │
│  • Processing Controls                  │
│  • Result Display                       │
└────────────────┬────────────────────────┘
                 │
         HTTP API Requests
                 │
                 ▼
┌─────────────────────────────────────────┐
│     Flask Backend (Port 5000)           │
│  • Image Processing                     │
│  • OpenCV Operations                    │
│  • Gradient Computation                 │
└─────────────────────────────────────────┘
```

### Processing Flow

1. **User uploads image** → React frontend
2. **Frontend checks backend** → `GET /health`
3. **Backend responds** → "I'm alive"
4. **User processes image** → Frontend sends to backend
5. **Backend processes** → OpenCV.js fallback if needed
6. **Returns result** → Frontend displays processed image

---

## What's Connected

### Frontend Features
- **Automatic Backend Detection**: Checks if backend is available on startup
- **Smart Fallback**: Uses browser-based OpenCV.js if backend unavailable
- **Status Indicator**: Shows "✅ Backend Connected" or "📡 Using Browser Processing"

### Backend Features
- **CORS Enabled**: Accepts requests from React frontend
- **Health Check**: `/health` endpoint for connectivity testing
- **Image Processing**: Handles Gradient, Sobel, and Canny detection
- **Base64 Support**: Accepts images as data URLs

---

## Environment Configuration

### `.env` File
```env
REACT_APP_API_URL=http://localhost:5000
FLASK_ENV=development
FLASK_DEBUG=False
```

**Modify if:**
- Backend runs on different port
- Backend on different machine
- Production deployment

---

## Testing the Connection

### 1. Check Backend Health
```bash
# In terminal or browser:
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy"}
```

### 2. Test Full Processing
```bash
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/png;base64,iVBORw0K...",
    "method": "gradient",
    "showGradientMagnitude": true,
    "showGradientDirection": false,
    "highlightLanes": true
  }'
```

### 3. Check Frontend Connectivity
- Open `http://localhost:3000`
- Look for status indicator in header
- Should say "✅ Backend Connected"
- Upload and process an image
- Should work without errors

---

## Common Issues & Solutions

### Issue: Backend not connecting
**Check:**
1. Is backend running? `http://localhost:5000/health`
2. Check .env file: `REACT_APP_API_URL=http://localhost:5000`
3. No firewall blocking port 5000
4. Backend started before frontend (or frontend will use fallback)

**Solution:**
```bash
# Terminal 1: Start backend first
cd backend
python app.py

# Terminal 2: Then start frontend
npm start
```

### Issue: CORS errors in console
**Solution:**
```bash
# Reinstall flask-cors
pip install --force-reinstall flask-cors
```

### Issue: "cv.phase is not a function"
**Status:** ✅ **FIXED** - Updated imageProcessing.js
- Uses only available OpenCV.js functions
- Falls back to backend for advanced operations

### Issue: Port 3000 or 5000 already in use
**Solution:**
```bash
# Change port in environment
PORT=3001 npm start

# Or kill existing process
lsof -ti:3000 | xargs kill -9
```

---

## Scripts Available

| Command | Purpose |
|---------|---------|
| `npm start` | Start React frontend only |
| `npm run backend` | Start Flask backend only |
| `npm run dev` | Start both in parallel |
| `npm build` | Build for production |
| `npm test` | Run tests |

---

## Development Workflow

### Making Frontend Changes
1. Edit React files in `src/`
2. Save automatically reloads (hot reload)
3. Backend continues running in parallel
4. No need to restart backend

### Making Backend Changes
1. Edit Python files in `backend/`
2. Manually restart backend (Ctrl+C, then `python app.py`)
3. Or restart entire dev environment
4. Frontend auto-refreshes after reconnection

### Adding New Processing Method
1. **Backend**: Add function to `backend/app.py`
2. **Backend**: Add route to `/process` endpoint
3. **Frontend**: Add to `src/utils/imageProcessing.js`
4. **Frontend**: Add UI option in `src/App.js`
5. **Test**: Upload image and try new method

---

## Production Deployment

### Using Docker Compose
```bash
# Start both services in containers
docker-compose up

# Stop services
docker-compose down
```

### Manual Production Setup
1. **Build React app**:
   ```bash
   npm run build
   ```

2. **Serve with web server** (Nginx/Apache):
   - Serve `build/` folder
   - Proxy `/api/*` to Flask backend

3. **Run Flask in production**:
   ```bash
   gunicorn backend:app
   ```

---

## Performance Tips

1. **Process on Backend**: Use backend for large images (> 2000px)
2. **Use Gradient Method**: Faster than Sobel/Canny
3. **Close Unused Apps**: Free up system resources
4. **Enable Hardware Acceleration**: Browser settings

---

## Monitoring

### Frontend Logs
- Open browser DevTools (F12)
- Console tab shows connection status
- Network tab shows API calls to backend

### Backend Logs
- Terminal output shows processing status
- Check for errors in Flask output
- Use `FLASK_DEBUG=True` for detailed logs

---

## Troubleshooting Commands

```bash
# Check if backend is running
curl http://localhost:5000/health

# Check if frontend is running
curl http://localhost:3000

# Check port usage
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000

# Restart everything
# Kill both processes (Ctrl+C)
# Run start.bat or start.sh again
```

---

## Next Steps

✅ Both frontend and backend are now integrated!

1. **Run the application**:
   - Windows: `start.bat`
   - Mac/Linux: `./start.sh`

2. **Upload a road/vehicle image**

3. **Try different detection methods**:
   - Gradient (fastest)
   - Sobel (balanced)
   - Canny (highest quality)

4. **Explore the code**:
   - React components in `src/components/`
   - Backend processing in `backend/app.py`
   - Image processing in `src/utils/imageProcessing.js`

---

## Support

- Check [README.md](README.md) for full documentation
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for architecture details

---

**You now have a fully integrated Lane Detection System!** 🚗✨
