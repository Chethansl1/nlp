# Troubleshooting Guide

Solutions for common issues encountered with the Lane Detection application.

## Setup Issues

### Issue: `npm install` fails

**Symptoms**: 
- Error messages about dependencies
- Network timeout errors
- "Cannot find module" errors

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete existing node_modules
rm -rf node_modules package-lock.json

# Reinstall from scratch
npm install

# If still failing, try using npm ci instead
npm ci
```

**Alternate**: Use yarn if available
```bash
yarn install
```

### Issue: Python virtual environment not working

**Symptoms**:
- `command not found: python`
- Virtual environment not activating
- Python version mismatch

**Solutions**:
```bash
# Check Python installation
python --version
python3 --version

# Create new virtual environment
python -m venv venv

# Windows - activate
venv\Scripts\activate.bat

# macOS/Linux - activate
source venv/bin/activate

# Verify activation (prompt should show (venv))
```

**If Python not found**:
- Download from python.org
- Ensure Python is in PATH
- Restart terminal after installation

### Issue: Port already in use

**Symptoms**:
- "Address already in use"
- "EADDRINUSE" error
- Cannot start development server

**Solutions**:
```bash
# Find process using port 3000 (React)
# macOS/Linux:
lsof -i :3000
# Kill the process
kill -9 <PID>

# Windows PowerShell:
Get-Process | Where-Object {$_.Port -eq 3000}
Stop-Process -Id <PID> -Force

# Or use different port
PORT=3001 npm start
```

**For Flask (port 5000)**:
```bash
# Change Flask port
python app.py --port 5001
```

## Frontend Issues

### Issue: OpenCV.js not loading

**Symptoms**:
- "cv is not defined" error in console
- Images won't process
- Blank console error

**Solutions**:
1. **Wait for OpenCV to load**:
   - OpenCV.js takes time to download (~8MB)
   - Wait 5-10 seconds after page load
   - Watch Network tab in DevTools

2. **Check internet connection**:
   - OpenCV loaded from CDN
   - Requires active internet
   - Check browser console for CORS errors

3. **Update CDN link**:
   - Edit `public/index.html`
   - Ensure URL is correct:
   ```html
   <script async src="https://docs.opencv.org/4.5.2/opencv.js"></script>
   ```

4. **Use offline OpenCV**:
   - Download opencv.js locally
   - Update script src path

### Issue: Image upload not working

**Symptoms**:
- Upload button doesn't respond
- "No file selected" error
- Wrong file type error

**Solutions**:
```javascript
// Verify file types in ImageUpload.js
<input accept="image/*" />  // Should accept all image formats

// Supported formats:
- JPG/JPEG
- PNG
- BMP
- WebP
- GIF
```

**If file selected but not uploading**:
- Check file size (should be reasonable)
- Try different image format
- Check browser console for errors

### Issue: Image processing fails

**Symptoms**:
- "Processing..." never completes
- Error after clicking Process button
- Blank processed image

**Solutions**:
```bash
# 1. Check browser console
# Open DevTools → Console → Look for errors

# 2. Reduce image size
# Large images (>4000px) may cause issues

# 3. Try simpler detection method
# Use Gradient (fastest) instead of Canny

# 4. Check available memory
# Open Task Manager → Performance
# If low on memory, close other apps

# 5. Try different image
# Some image formats may not work
```

### Issue: Page loads but nothing displays

**Symptoms**:
- Blank white page
- "Failed to compile" error
- Only header visible

**Solutions**:
```bash
# Check for build errors
npm start

# If compile error shown:
# 1. Fix syntax errors
# 2. Check imports are correct
# 3. Verify component files exist

# Clear React cache
rm -rf node_modules/.cache
npm start

# Try hard refresh
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (macOS)
```

### Issue: Styling looks broken

**Symptoms**:
- Colors wrong
- Layout messed up
- No animations

**Solutions**:
```bash
# 1. Verify CSS file is loaded
# DevTools → Elements → check <link> tag

# 2. Check CSS file path in index.html
<link rel="stylesheet" href="../src/index.css">

# 3. Rebuild if needed
npm run build

# 4. Clear browser cache
# DevTools → Settings → Application → Clear site data

# 5. Check for CSS errors
# DevTools → Sources → Look for CSS issues
```

### Issue: Tabs not switching

**Symptoms**:
- Tab buttons don't respond
- Image doesn't change when clicking tabs
- Only one image visible

**Solutions**:
```javascript
// Check ProcessedImage.js component
// Verify tab button onClick handlers

// If processedImage is null, tabs won't show
// Make sure process is complete first

// Try different method
// May need to reprocess with different settings
```

## Backend Issues

### Issue: Flask server won't start

**Symptoms**:
- "No module named flask" error
- Import errors
- Server crashes immediately

**Solutions**:
```bash
# 1. Verify virtual environment is activated
# Should show (venv) in prompt

# 2. Install Flask and dependencies
pip install -r backend/requirements.txt

# 3. Check Python version
python --version  # Should be 3.8+

# 4. Reinstall packages
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall

# 5. Check for syntax errors
python -m py_compile backend/app.py
```

### Issue: Backend API not responding

**Symptoms**:
- `/process` endpoint returns error
- CORS errors in browser console
- "Connection refused"

**Solutions**:
```bash
# 1. Verify backend is running
# Check terminal for "Running on http://localhost:5000"

# 2. Check API URL in React
# .env should have: REACT_APP_API_URL=http://localhost:5000

# 3. Enable CORS
# Verify flask_cors is installed:
pip install flask-cors

# 4. Check firewall
# Windows Firewall may block port 5000
# Add Flask to firewall exceptions

# 5. Test endpoint manually
curl http://localhost:5000/health
# Should return: {"status": "healthy"}
```

### Issue: Image processing on backend fails

**Symptoms**:
- Response: {"error": "..."}
- Backend logs show errors
- Processed image is blank

**Solutions**:
```python
# 1. Check for OpenCV import
python -c "import cv2; print(cv2.__version__)"

# 2. Reinstall OpenCV
pip install --upgrade opencv-python

# 3. Check image format
# Verify image is valid base64

# 4. Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# 5. Test processing directly
from PIL import Image
import cv2
import numpy as np
# Test a local image processing
```

### Issue: Out of memory error

**Symptoms**:
- Process fails for large images
- Memory usage keeps growing
- Backend crashes

**Solutions**:
```python
# backend/image_processing.py
# Add image resizing:
def process_image(self, image, method='gradient', options=None):
    # Resize if too large
    max_dimension = 2000
    height, width = image.shape[:2]
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        new_size = (int(width * scale), int(height * scale))
        image = cv2.resize(image, new_size)
    
    # ... rest of processing
```

## Docker Issues

### Issue: Docker containers won't start

**Symptoms**:
- `docker-compose up` fails
- Container exits immediately
- Build errors

**Solutions**:
```bash
# 1. Check Docker is installed
docker --version
docker-compose --version

# 2. Rebuild images
docker-compose down
docker-compose build --no-cache

# 3. Check logs
docker-compose logs

# 4. Verify Dockerfile paths
# Check all Dockerfile references are correct

# 5. Free up space
docker system prune
docker system prune -a  # Remove all unused images
```

### Issue: Port conflicts in Docker

**Symptoms**:
- "Address already in use" from Docker
- Cannot access services on expected ports

**Solutions**:
```bash
# 1. Check running containers
docker ps

# 2. Stop conflicting container
docker stop <container_id>

# 3. Edit docker-compose.yml ports
services:
  frontend:
    ports:
      - "3001:3000"  # Changed from 3000:3000
  backend:
    ports:
      - "5001:5000"  # Changed from 5000:5000
```

## Git Issues

### Issue: Git clone fails

**Symptoms**:
- "Repository not found"
- Permission denied errors
- Timeout during clone

**Solutions**:
```bash
# 1. Check internet connection
ping github.com

# 2. Verify repository URL
git clone https://github.com/username/cv.git

# 3. Set up SSH if HTTPS fails
ssh-keygen -t ed25519
# Add public key to GitHub

# 4. Use different protocol
# Try HTTPS if SSH fails or vice versa
```

### Issue: Merge conflicts

**Symptoms**:
- Cannot pull latest changes
- Conflicts in files

**Solutions**:
```bash
# 1. Stash current changes
git stash

# 2. Pull latest
git pull origin main

# 3. Reapply changes
git stash pop

# 4. Resolve conflicts manually
# Edit conflicted files
# Remove conflict markers (<<< === >>>)
# git add and commit
```

## Performance Issues

### Issue: Slow image processing

**Symptoms**:
- Processing takes >5 seconds
- High CPU usage
- Browser unresponsive

**Solutions**:
1. **Use Gradient method**: Fastest option
2. **Reduce image size**: 
   - Resize before upload
   - Recommend < 1920x1080
3. **Close other apps**: Free up system resources
4. **Enable hardware acceleration**: Browser settings
5. **Use backend**: Flask backend may be faster for large images

### Issue: High memory usage

**Symptoms**:
- Browser memory constantly increasing
- Computer slowing down
- "Out of memory" crashes

**Solutions**:
```javascript
// imageProcessing.js - Ensure cleanup
function processImageWithOpenCV(imageSource, options) {
  // ... processing code ...
  
  // Always cleanup OpenCV objects
  if (src) src.delete();
  if (dst) dst.delete();
  if (gradX) gradX.delete();
  if (gradY) gradY.delete();
  
  // Return result
  return processedImage;
}

// Restart browser if memory grows too much
```

## Logging and Debugging

### Enable Debug Logging

**Frontend**:
```javascript
// In browser console:
localStorage.debug = 'app:*'
location.reload()
```

**Backend**:
```python
# In app.py:
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment:
export FLASK_DEBUG=True
python app.py
```

### Inspect Network Requests

1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Upload and process image
5. Look for:
   - Failed requests (red)
   - Large response times
   - CORS errors

### Check Browser Compatibility

```bash
# Test different browsers
# Use browserstack or similar service
# Check console for compatibility warnings
```

## Contact Support

If issues persist:

1. **Check Documentation**:
   - [README.md](README.md)
   - [SETUP_GUIDE.md](SETUP_GUIDE.md)
   - [DEVELOPMENT.md](DEVELOPMENT.md)

2. **Search Issues**: GitHub issues/discussions

3. **Create Detailed Issue**:
   - OS and version
   - Browser and version
   - Steps to reproduce
   - Error messages
   - Screenshots

4. **Provide Logs**:
   - Browser console logs
   - Backend logs
   - Docker logs (if applicable)

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| npm error | `npm cache clean --force && npm install` |
| Port in use | `lsof -i :3000` and `kill -9 <PID>` |
| OpenCV not loading | Wait 10s, check internet, check CDN URL |
| Flask not starting | `pip install -r requirements.txt` |
| Image won't process | Reduce size, try different method |
| Styles broken | Clear cache, check CSS path |
| Docker error | `docker-compose down && docker-compose build` |

---

**Last Updated**: 2024
