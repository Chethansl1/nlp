# Quick Start Guide

Get the Lane Detection app running in 5 minutes!

## Option 1: Frontend Only (⭐ Fastest)

```bash
npm install
npm start
```

✅ App opens at `http://localhost:3000`

## Option 2: Frontend + Backend (Complete)

### Terminal 1: Frontend
```bash
npm install
npm start
```

### Terminal 2: Backend
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

✅ Frontend: `http://localhost:3000`
✅ Backend: `http://localhost:5000`

## Option 3: Docker (One Command)

```bash
docker-compose up
```

✅ Both services start automatically

---

## First Run Steps

1. Open app at `http://localhost:3000`
2. Click **📷 Upload Image**
3. Select a road/vehicle image
4. Click **Process Image**
5. View results in tabs
6. Read discussion points below

## What to Try

### Edge Detection Methods
- **Gradient** (fastest): Basic edge detection
- **Sobel**: Better edge definition
- **Canny** (best): Highest quality, slightly slower

### Options
- ✓ Show Gradient Magnitude
- ✓ Show Gradient Direction  
- ✓ Highlight Lane Markings

## Recommended Test Images

- Road with lane markings
- Vehicle from above
- Highway scenes
- Urban roads with clear edges

## File Paths

| File | Purpose |
|------|---------|
| `src/App.js` | Main component |
| `src/utils/imageProcessing.js` | OpenCV.js integration |
| `backend/app.py` | Flask API |
| `src/index.css` | Styling |

## Common Commands

```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm build

# Install Python packages
pip install -r backend/requirements.txt

# Run Flask
python backend/app.py

# Docker commands
docker-compose up          # Start all services
docker-compose down        # Stop all services
docker-compose logs        # View logs
```

## Need Help?

- **Frontend issues**: Check `src/` directory
- **Backend issues**: Check `backend/` directory
- **Setup issues**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Development**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Full docs**: See [README.md](README.md)

## System Requirements

- Node.js 16+ OR Docker
- Python 3.8+ (for backend only)
- Modern browser (Chrome, Firefox, Safari, Edge)
- ~500MB disk space

---

**That's it! You're ready to go.** 🚀
