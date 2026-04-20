# Project Manifest

Complete file structure and description of the Autonomous Vehicle Lane Detection application.

## Overview

A React-based web application for analyzing vehicle road images using OpenCV.js for real-time gradient computation and edge detection. Includes optional Flask backend for enhanced image processing flexibility.

## Root Directory Files

| File | Purpose |
|------|---------|
| `package.json` | Frontend dependencies and scripts |
| `.gitignore` | Git ignore patterns |
| `.env.example` | Environment variables template |
| `README.md` | Main project documentation |
| `SETUP_GUIDE.md` | Detailed setup instructions |
| `DEVELOPMENT.md` | Developer guide and architecture |
| `QUICK_START.md` | 5-minute quick start |
| `PROJECT_MANIFEST.md` | This file - complete file listing |
| `Dockerfile` | Combined Docker configuration |
| `Dockerfile.frontend` | Frontend Docker configuration |
| `docker-compose.yml` | Docker Compose orchestration |

## Frontend Structure (`src/`)

### Core Files

| File | Size | Purpose |
|------|------|---------|
| `index.js` | 265 B | React entry point, mounts App component |
| `App.js` | 4.93 KB | Main React component, state management |
| `index.css` | 5.48 KB | Global styles, animations, responsive design |

### Components (`src/components/`)

| Component | Size | Purpose |
|-----------|------|---------|
| `ImageUpload.js` | 960 B | Image file upload interface |
| `ProcessedImage.js` | 2.22 KB | Image display with tab switching |
| `DiscussionPoints.js` | 3.04 KB | Educational content about gradient computation |

**Component Hierarchy**:
```
App
├── ImageUpload (image selection)
├── ProcessedImage (display & tabs)
└── DiscussionPoints (information)
```

### Utilities (`src/utils/`)

| File | Size | Purpose |
|------|------|---------|
| `imageProcessing.js` | 5.03 KB | OpenCV.js image processing functions |
| `api.js` | 1.14 KB | Backend API communication (optional) |

## Public Files (`public/`)

| File | Purpose |
|------|---------|
| `index.html` | HTML template with OpenCV.js CDN link |

## Backend Structure (`backend/`)

| File | Size | Purpose |
|------|------|---------|
| `app.py` | 4.44 KB | Flask application, API routes, image processing |
| `image_processing.py` | 4 KB | Reusable image processing utilities, LaneDetector class |
| `config.py` | 708 B | Configuration management (dev, prod, test) |
| `requirements.txt` | 88 B | Python dependencies |
| `Dockerfile` | 309 B | Docker configuration for backend |

## Key Technologies

### Frontend
- **React 18.2.0**: UI framework
- **OpenCV.js 4.5.2**: Browser-based image processing (from CDN)
- **CSS3**: Responsive design, animations

### Backend
- **Flask 2.3.0**: Web framework
- **OpenCV (cv2) 4.7.0**: Advanced image processing
- **NumPy 1.24.3**: Numerical operations
- **Pillow 9.5.0**: Image manipulation
- **Flask-CORS 4.0.0**: Cross-origin support

## File Dependencies

### Image Processing Pipeline

```
ImageUpload
    ↓
App (state management)
    ↓
ProcessedImage (display)
    ↓
imageProcessing.js (OpenCV.js)
    ↓ (optional)
api.js → app.py (Flask backend)
```

### Data Flow

1. **User uploads image** → ImageUpload component
2. **Image stored in state** → App component
3. **User clicks Process** → imageProcessing.js or api.js
4. **OpenCV processes** → Returns processed image
5. **Display in tabs** → ProcessedImage component

## Component Responsibilities

### App.js
- ✓ Main state container
- ✓ Image upload handling
- ✓ Processing orchestration
- ✓ Error handling
- ✓ UI coordination

### ImageUpload.js
- ✓ File input interface
- ✓ File validation
- ✓ Upload triggering
- ✓ Error feedback

### ProcessedImage.js
- ✓ Image display
- ✓ Tab switching
- ✓ Processing info display
- ✓ Original/Processed comparison

### DiscussionPoints.js
- ✓ Educational content
- ✓ Gradient computation explanation
- ✓ Lane detection importance
- ✓ Computer vision fundamentals

### imageProcessing.js
- ✓ OpenCV.js initialization
- ✓ Gradient computation
- ✓ Sobel edge detection
- ✓ Canny edge detection
- ✓ Lane highlighting
- ✓ Image normalization

### app.py (Backend)
- ✓ Flask API server
- ✓ Image processing routes
- ✓ CORS support
- ✓ Health check endpoint
- ✓ Base64 image handling

## Processing Functions

### Frontend (imageProcessing.js)

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `processImageWithOpenCV()` | Image, options | Data URL | Main processing pipeline |
| `computeGradient()` | Mat | Gradient image | Gradient magnitude/direction |
| `computeSobel()` | Mat | Edge map | Sobel edge detection |
| `computeCanny()` | Mat | Edge map | Canny edge detection |
| `highlightLaneMarkings()` | Mat, Mat | Colored image | Lane highlighting |
| `normalizeAndConvert()` | Mat | Display image | Image normalization |

### Backend (app.py)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/process` | POST | Process image with specified method |
| `/health` | GET | Health check |

### Backend (image_processing.py)

| Class | Methods | Purpose |
|-------|---------|---------|
| `LaneDetector` | compute_gradient | Gradient computation |
| | compute_sobel_edges | Sobel detection |
| | compute_canny_edges | Canny detection |
| | highlight_lane_markings | Lane highlighting |
| | detect_vehicle_edges | Vehicle detection |

## Configuration Files

### package.json
- React scripts and dependencies
- Development/build/test commands
- ESLint configuration

### backend/requirements.txt
- Flask 2.3.0
- opencv-python 4.7.0.72
- numpy 1.24.3
- Pillow 9.5.0
- flask-cors 4.0.0

### docker-compose.yml
- Frontend service (port 3000)
- Backend service (port 5000)
- Volume mounts
- Environment variables

## Styling

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.app-container` | Main container |
| `.header` | Title section |
| `.main-container` | Two-column layout |
| `.panel` | Content panels |
| `.upload-panel` | Upload/controls section |
| `.display-panel` | Image display section |
| `.discussion-panel` | Information section |
| `.image-container` | Image display area |
| `.tab-buttons` | Tab navigation |
| `.processing-info` | Info message |
| `.discussion-points` | Discussion items |
| `.error-message` | Error display |
| `.success-message` | Success display |
| `.loading-spinner` | Loading animation |

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

### Backend (app.py)
```
FLASK_ENV=development
FLASK_DEBUG=True
```

## File Sizes Summary

| Category | Total |
|----------|-------|
| React Components | 11.2 KB |
| Utilities | 6.17 KB |
| Styles | 5.48 KB |
| Backend Python | ~9 KB |
| Config Files | 1.5 KB |
| Docs | ~25 KB |

**Total: ~60 KB** (before dependencies)

## Edge Detection Methods

### Gradient (computeGradient)
- Sobel filters for X and Y
- Magnitude: √(Gx² + Gy²)
- Direction: atan2(Gy, Gx)
- Fast, suitable for real-time

### Sobel (computeSobel)
- Combined gradient magnitude
- Threshold binarization
- Faster than Canny

### Canny (computeCanny)
- Gaussian blur preprocessing
- Non-maximum suppression
- Hysteresis thresholding
- Highest quality, slowest

## Processing Pipeline

```
Original Image
    ↓
Convert to Grayscale
    ↓
Apply Edge Detection
├── Gradient Method
│   ├── Compute gradients
│   ├── Calculate magnitude
│   └── Calculate direction
├── Sobel Method
│   ├── Sobel filters
│   ├── Magnitude combination
│   └── Thresholding
└── Canny Method
    ├── Gaussian blur
    ├── Edge detection
    └── Thinning
    ↓
Lane Highlighting
├── Threshold magnitude
├── Morphological ops
└── Contour detection
    ↓
Normalize for Display
    ↓
Display Result
```

## Browser Support

| Browser | Min Version | Status |
|---------|------------|--------|
| Chrome | 90+ | ✅ Full support |
| Firefox | 88+ | ✅ Full support |
| Safari | 14+ | ✅ Full support |
| Edge | 90+ | ✅ Full support |
| Opera | 76+ | ✅ Full support |
| IE | Any | ❌ Not supported |

## Deployment Targets

- Local development
- Docker containers
- AWS ECS/Fargate
- Heroku
- Google Cloud Run
- Azure Container Instances

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial release |

## Repository Structure

```
cv/
├── src/                    # React source
│   ├── components/         # React components
│   ├── utils/             # Utility functions
│   ├── App.js             # Main app
│   ├── index.js           # Entry point
│   └── index.css          # Global styles
├── backend/               # Flask backend
│   ├── app.py             # Flask app
│   ├── image_processing.py # Processing logic
│   ├── config.py          # Configuration
│   ├── requirements.txt    # Dependencies
│   └── Dockerfile         # Backend Docker
├── public/                # Static files
│   └── index.html         # HTML template
├── node_modules/          # Frontend deps (after npm install)
├── build/                 # Production build (after npm build)
├── package.json           # Project config
├── .gitignore             # Git ignore
├── .env.example           # Env template
├── Dockerfile             # Main Docker
├── Dockerfile.frontend    # Frontend Docker
├── docker-compose.yml     # Docker Compose
├── README.md              # Main docs
├── SETUP_GUIDE.md         # Setup instructions
├── DEVELOPMENT.md         # Dev guide
├── QUICK_START.md         # Quick start
└── PROJECT_MANIFEST.md    # This file
```

## Next Steps

1. ✅ Project created
2. → Install dependencies: `npm install`
3. → Start app: `npm start`
4. → Upload image and test
5. → Explore code
6. → Customize features

---

**Complete, production-ready project structure** ✨
