# How to Run the Application

## ⚡ Quick Start (Recommended)

### Windows
Double-click this file:
```
start.bat
```

### macOS/Linux
Run this in terminal:
```bash
chmod +x start.sh
./start.sh
```

**That's it!** Both frontend and backend will start automatically.

---

## What Happens When You Run It

1. ✅ Checks Node.js and Python installation
2. ✅ Installs npm dependencies (if needed)
3. ✅ Creates Python virtual environment (if needed)
4. ✅ Installs Python dependencies (if needed)
5. ✅ Starts React frontend → `http://localhost:3000`
6. ✅ Starts Flask backend → `http://localhost:5000`
7. ✅ Browser opens to the app

**Total time:** ~2-3 minutes on first run, ~10 seconds on subsequent runs

---

## Alternative: Manual Run

### Terminal 1 - Frontend
```bash
npm install    # First time only
npm start
```

### Terminal 2 - Backend
```bash
cd backend
python -m venv venv              # First time only

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt  # First time only
python app.py
```

---

## Usage Steps

1. **Open** → `http://localhost:3000`
2. **Upload** → Click "📷 Upload Image" (road/vehicle image)
3. **Configure** → Choose detection method:
   - Gradient (⚡ fastest)
   - Sobel (balanced)
   - Canny (🔥 best quality)
4. **Process** → Click "Process Image"
5. **View** → Switch tabs to see results
6. **Learn** → Read discussion points below

---

## Detection Methods Explained

### 🟢 Gradient (Fastest)
- Speed: ⚡⚡⚡ Very fast
- Quality: ⭐⭐⭐ Good
- Use for: Real-time processing, large images
- Shows: Gradient magnitude and direction

### 🟡 Sobel (Balanced)
- Speed: ⚡⚡ Medium
- Quality: ⭐⭐⭐⭐ Very good
- Use for: General edge detection
- Shows: Combined gradient edges

### 🔴 Canny (Best Quality)
- Speed: ⚡ Slower
- Quality: ⭐⭐⭐⭐⭐ Excellent
- Use for: High-quality lane detection
- Shows: Thin, connected edges

---

## Features

✅ **Real-time Image Processing** - Upload and process in browser  
✅ **Multiple Edge Detection Methods** - Choose what works best  
✅ **Lane Highlighting** - Automatically highlights lane markings  
✅ **Dual Processing** - Frontend OR backend processing  
✅ **Educational Content** - Learn why gradients matter  
✅ **Responsive Design** - Works on desktop and tablet  

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|------------|
| OS | Windows/Mac/Linux | Latest version |
| RAM | 4GB | 8GB+ |
| Node.js | 16.x | 18.x LTS |
| Python | 3.8 | 3.9+ |
| Browser | Chrome 90+ | Latest |

---

## Troubleshooting

### "Port already in use"
```bash
# Kill process using port 3000 or 5000
# Windows: TaskManager → End process
# Mac/Linux: lsof -ti:3000 | xargs kill -9
```

### "cv.phase is not a function"
✅ **Already Fixed!** - Uses backend processing instead

### "Backend not connecting"
- Check: Is backend running on port 5000?
- Check: Firewall blocking port 5000?
- Fallback: App uses browser processing if backend unavailable

### Dependencies won't install
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Upload image | Click button or Ctrl+U |
| Process | Enter key |
| Stop processing | Esc |
| Refresh | F5 |
| Developer tools | F12 |

---

## File Structure

```
cv/
├── start.bat          ← Run this on Windows
├── start.sh           ← Run this on Mac/Linux
├── src/               ← React source code
│   ├── App.js        ← Main app
│   ├── index.css     ← Styling
│   └── components/   ← React components
├── backend/           ← Flask backend
│   ├── app.py        ← Backend server
│   └── requirements.txt
├── public/
│   └── index.html    ← HTML template
└── package.json      ← Project config
```

---

## Performance Tips

1. **Use Gradient for speed**: 3-5x faster than Canny
2. **Resize large images**: Keep < 2000px on longest side
3. **Close other apps**: More memory for processing
4. **Use Chrome/Edge**: Faster than Firefox/Safari
5. **Backend for large images**: More powerful than browser

---

## API Endpoints (Backend)

### Process Image
```
POST http://localhost:5000/process
Content-Type: application/json

{
  "image": "data:image/png;base64,...",
  "method": "gradient|sobel|canny",
  "showGradientMagnitude": true,
  "showGradientDirection": false,
  "highlightLanes": true
}

Response:
{
  "success": true,
  "processedImage": "data:image/png;base64,...",
  "method": "gradient"
}
```

### Health Check
```
GET http://localhost:5000/health

Response:
{
  "status": "healthy"
}
```

---

## Development Mode

### Make Changes
- **React**: Edit `src/*.js`, auto-reloads
- **Backend**: Edit `backend/app.py`, restart needed

### Debug
- **Frontend**: Open DevTools (F12)
- **Backend**: Check terminal output

### Test
```bash
npm test                    # React tests
pytest backend/             # Python tests
```

---

## Production Deployment

### Docker
```bash
docker-compose up
```

### Manual
```bash
npm run build              # Build React app
gunicorn backend:app       # Run Flask with gunicorn
```

---

## Support & Help

📖 **Full Documentation**: See [README.md](README.md)  
🔧 **Setup Guide**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)  
🐛 **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
🏗️ **Architecture**: See [DEVELOPMENT.md](DEVELOPMENT.md)  
🔗 **Integration**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)  

---

## Common Commands

```bash
# First time setup
start.bat                 # Windows
./start.sh               # Mac/Linux

# Restart
Ctrl+C                   # Stop current run
start.bat               # Windows - restart
./start.sh              # Mac/Linux - restart

# Manual control
npm start                # React only
npm run backend          # Flask only
npm run dev              # Both (if setup)

# Cleanup
rm -rf node_modules      # Remove npm packages
rm -rf backend/venv      # Remove Python venv
```

---

## Success Checklist

Before uploading an image:

- [ ] Browser shows "✅ Backend Connected" in header
- [ ] No red errors in browser console (F12)
- [ ] Backend terminal shows "Running on http://localhost:5000"
- [ ] Can access http://localhost:3000
- [ ] Upload button appears and works

---

## Next Steps

1. ✅ Run `start.bat` or `./start.sh`
2. ✅ Upload a road/vehicle image
3. ✅ Try different detection methods
4. ✅ Read the discussion points
5. ✅ Explore the code
6. ✅ Customize for your needs

---

**Your Lane Detection System is ready! 🚗✨**

Start with: `start.bat` (Windows) or `./start.sh` (Mac/Linux)
