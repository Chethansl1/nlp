# Setup Guide - Autonomous Vehicle Lane Detection

This guide provides step-by-step instructions for setting up and running the application.

## Prerequisites

- Node.js 16+ (for React frontend)
- Python 3.8+ (for Flask backend)
- Git (for cloning the repository)
- Modern web browser with WebAssembly support

## Quick Start

### Option 1: Frontend Only (Recommended for beginners)

The frontend uses OpenCV.js loaded from CDN, so you can run it without the backend.

#### Windows
```bash
# Install dependencies
npm install

# Start the development server
npm start
```

The application will open at `http://localhost:3000`

#### macOS/Linux
```bash
npm install
npm start
```

### Option 2: Frontend + Backend

#### Step 1: Start Frontend

```bash
# Terminal 1: Frontend
npm install
npm start
```

#### Step 2: Start Backend

```bash
# Terminal 2: Backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

The frontend will run at `http://localhost:3000`
The backend will run at `http://localhost:5000`

### Option 3: Docker (Recommended for deployment)

#### Using Docker Compose (Easiest)

```bash
docker-compose up
```

This starts both frontend and backend in containers.

#### Using Individual Docker Images

```bash
# Build frontend image
docker build -f Dockerfile.frontend -t lane-detection-frontend .

# Build backend image
docker build -f backend/Dockerfile -t lane-detection-backend ./backend

# Run frontend
docker run -p 3000:3000 lane-detection-frontend

# Run backend
docker run -p 5000:5000 lane-detection-backend
```

## Project Structure

```
cv/
├── src/                          # React source files
│   ├── components/
│   │   ├── ImageUpload.js        # Image upload component
│   │   ├── ProcessedImage.js     # Image display component
│   │   └── DiscussionPoints.js   # Discussion points component
│   ├── utils/
│   │   ├── imageProcessing.js    # OpenCV.js image processing
│   │   └── api.js                # Backend API calls
│   ├── App.js                    # Main React component
│   ├── index.js                  # React entry point
│   └── index.css                 # Styling
├── public/
│   └── index.html                # HTML template
├── backend/
│   ├── app.py                    # Flask application
│   ├── image_processing.py       # Image processing utilities
│   ├── config.py                 # Configuration
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                # Backend Docker configuration
├── package.json                  # Frontend dependencies
├── Dockerfile                    # Combined Docker configuration
├── Dockerfile.frontend           # Frontend Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```

## Available Scripts

### Frontend Scripts

```bash
npm start       # Start development server (port 3000)
npm build       # Build for production
npm test        # Run tests
npm eject       # Eject from Create React App (irreversible)
```

### Backend Scripts

```bash
python app.py                    # Run Flask development server
python -m pytest                # Run tests (if configured)
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

For backend, set:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
```

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome/Chromium | 90+ | ✅ Supported |
| Firefox | 88+ | ✅ Supported |
| Safari | 14+ | ✅ Supported |
| Edge | 90+ | ✅ Supported |
| Opera | 76+ | ✅ Supported |
| IE 11 | N/A | ❌ Not Supported |

## Troubleshooting

### Issue: OpenCV.js not loading

**Solution:**
- Check internet connection (OpenCV.js is loaded from CDN)
- Wait a few seconds after page load
- Check browser console for errors
- Try a different browser

### Issue: npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: Port already in use

**Solution:**
```bash
# Find and kill process on port 3000 (React)
lsof -ti:3000 | xargs kill -9

# Find and kill process on port 5000 (Flask)
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: Python virtual environment not activating

**Solution:**
```bash
# Delete and recreate virtual environment
rm -rf venv
python -m venv venv

# Activate again
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Issue: Flask CORS errors

**Solution:**
- Make sure `flask-cors` is installed: `pip install flask-cors`
- Verify Flask is running on correct port
- Check API URL in React .env file

## Performance Optimization

### Frontend
1. Use images up to 1920x1080 for optimal performance
2. Enable browser hardware acceleration
3. Close unnecessary tabs
4. Use Gradient method (faster than Canny)

### Backend
1. Use GPU acceleration if available
2. Optimize image size before processing
3. Cache results for similar images
4. Monitor memory usage with large images

## Development Workflow

### Frontend Development

1. **Component Development**
   ```bash
   npm start
   ```
   - Hot reload enabled
   - Open browser console for debugging
   - Use React Developer Tools extension

2. **Testing**
   ```bash
   npm test
   ```

3. **Production Build**
   ```bash
   npm build
   ```

### Backend Development

1. **Run with Debug**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=True
   python app.py
   ```

2. **Testing**
   ```bash
   pytest backend/
   ```

3. **Code Style**
   ```bash
   pip install flake8
   flake8 backend/
   ```

## Deployment

### AWS Deployment

```bash
# Build Docker image
docker build -t lane-detection .

# Tag for ECR
docker tag lane-detection:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/lane-detection:latest

# Push to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/lane-detection:latest
```

### Heroku Deployment

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create lane-detection-app

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Local Deployment with Nginx

```bash
# Build React app
npm run build

# Configure Nginx to serve build folder
# and proxy /api requests to Flask backend
```

## Monitoring and Logging

### Frontend Logging

```javascript
// In browser console
localStorage.debug = 'app:*'
```

### Backend Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

1. Upload a test image of a road
2. Try different edge detection methods
3. Explore the discussion points
4. Customize the processing parameters
5. Integrate with your own models/systems

## Support and Contributions

- Report issues: Create a GitHub issue
- Contribute: Submit pull requests
- Feedback: Open discussions

## Resources

- [React Documentation](https://react.dev)
- [OpenCV.js Docs](https://docs.opencv.org/4.5.2/d5/d10/tutorial_js_root.html)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Autonomous Driving Resources](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013)

---

For more information, see [README.md](README.md)
