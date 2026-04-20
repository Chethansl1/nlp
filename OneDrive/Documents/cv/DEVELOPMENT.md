# Development Guide

This guide provides detailed information for developers working on the Autonomous Vehicle Lane Detection application.

## Architecture Overview

### Frontend Architecture

```
App Component (Main)
├── ImageUpload Component
├── ProcessedImage Component
├── DiscussionPoints Component
└── Image Processing Engine (OpenCV.js)
```

### Backend Architecture

```
Flask Application
├── Image Processing Module
├── API Routes
└── Configuration
```

## Component Details

### ImageUpload Component

**Purpose**: Handle image file selection and validation

**Key Props**:
- `onImageUpload`: Callback when image is selected

**State Management**: Uses parent component state

**Features**:
- File type validation
- File size checking
- Error handling

### ProcessedImage Component

**Purpose**: Display and switch between original and processed images

**Key Props**:
- `originalImage`: Original image data URL
- `processedImage`: Processed image data URL
- `currentType`: Currently displayed image type
- `onTypeChange`: Callback for tab switching

**Tabs**:
- Original: Shows input image
- Gradient: Gradient-based edge detection result
- Sobel: Sobel edge detection result
- Canny: Canny edge detection result

### DiscussionPoints Component

**Purpose**: Display educational content about gradient computation

**Content Areas**:
1. Importance of Gradient Computation
2. Feature Detection for Lane Following
3. Obstacle Detection and Boundary Identification
4. Sobel vs Canny Edge Detection
5. Robustness in Variable Lighting
6. Real-time Processing Requirements

## Image Processing Pipeline

### Step 1: Image Input
- Read image from file upload or canvas
- Validate image format and size

### Step 2: Preprocessing
- Convert to grayscale
- Optional: Gaussian blur for noise reduction

### Step 3: Gradient Computation
```
grad_x = Sobel(image, x-direction)
grad_y = Sobel(image, y-direction)
magnitude = sqrt(grad_x² + grad_y²)
direction = atan2(grad_y, grad_x)
```

### Step 4: Edge Detection
- **Gradient Method**: Direct magnitude thresholding
- **Sobel Method**: Combined gradient magnitude
- **Canny Method**: Multi-stage edge detection

### Step 5: Feature Enhancement
- Morphological operations (closing, dilation)
- Contour detection
- Lane marking highlighting

### Step 6: Output
- Normalize to 0-255 range
- Convert to display format
- Return as data URL

## API Endpoints

### POST /process

Processes an image on the backend.

**Request**:
```json
{
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "method": "gradient|sobel|canny",
  "showGradientMagnitude": true,
  "showGradientDirection": false,
  "highlightLanes": true
}
```

**Response**:
```json
{
  "success": true,
  "processedImage": "data:image/png;base64,iVBORw0KGgo...",
  "method": "selected_method"
}
```

**Error Response**:
```json
{
  "error": "Error message"
}
```

### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

## Adding New Features

### Adding a New Edge Detection Method

1. **Add to backend** (`backend/app.py`):
```python
def compute_custom_detection(image):
    # Your implementation here
    return processed_image

# Add to /process route
elif method == 'custom':
    result = compute_custom_detection(image)
```

2. **Add to frontend** (`src/utils/imageProcessing.js`):
```javascript
function computeCustomDetection(src) {
    // OpenCV.js implementation
    return dst;
}

// Add to processImageWithOpenCV
else if (options.method === 'custom') {
    dst = computeCustomDetection(src);
}
```

3. **Update UI** (`src/App.js`):
```javascript
<option value="custom">Custom Detection</option>
```

### Adding a New Control Option

1. **Add state in App.js**:
```javascript
const [newOption, setNewOption] = useState(false);
```

2. **Add UI element**:
```jsx
<div className="control-group">
  <label>
    <input
      type="checkbox"
      checked={newOption}
      onChange={(e) => setNewOption(e.target.checked)}
    />
    {' '}New Option
  </label>
</div>
```

3. **Pass to processing function**:
```javascript
await processImageWithOpenCV(originalImage, {
  // ... other options
  newOption,
});
```

### Adding a New Discussion Point

1. **Edit** `src/components/DiscussionPoints.js`:
```javascript
const points = [
  // ... existing points
  {
    title: 'Your Topic',
    content: 'Your detailed explanation...',
  },
];
```

## Performance Optimization

### Frontend Optimization

1. **Canvas Optimization**:
   - Use `createImageBitmap()` for better performance
   - Implement WebWorkers for heavy processing

2. **Memory Management**:
   - Properly delete OpenCV Mat objects
   - Clear old canvas data

3. **Image Processing**:
   - Resize images before processing
   - Use lower resolution for real-time processing

### Backend Optimization

1. **Image Preprocessing**:
   ```python
   # Resize if too large
   if max(image.shape) > 1920:
       scale = 1920 / max(image.shape)
       new_size = (int(image.shape[1] * scale), int(image.shape[0] * scale))
       image = cv2.resize(image, new_size)
   ```

2. **Caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=10)
   def process_cached(image_hash, method):
       # Processing logic
   ```

3. **GPU Acceleration**:
   - Use CUDA for OpenCV operations
   - Enable GPU acceleration in PyTorch/TensorFlow if needed

## Testing

### Frontend Testing

```bash
# Create test file: src/components/__tests__/ImageUpload.test.js
import { render, screen } from '@testing-library/react';
import ImageUpload from '../ImageUpload';

test('renders upload button', () => {
  render(<ImageUpload onImageUpload={jest.fn()} />);
  expect(screen.getByText(/Upload Image/i)).toBeInTheDocument();
});
```

### Backend Testing

```python
# Create test file: backend/test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## Debugging

### Frontend Debugging

1. **React Developer Tools**:
   - Install React DevTools extension
   - Inspect components and state

2. **Console Logging**:
   ```javascript
   console.log('Debug message:', variable);
   console.error('Error:', error);
   ```

3. **Network Debugging**:
   - Open DevTools Network tab
   - Monitor API calls to backend

### Backend Debugging

1. **Flask Debug Mode**:
   ```bash
   export FLASK_DEBUG=True
   python app.py
   ```

2. **Logging**:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug('Debug message')
   logger.error('Error message')
   ```

3. **Python Debugger**:
   ```python
   import pdb
   pdb.set_trace()  # Breakpoint
   ```

## Code Style

### JavaScript/React

```javascript
// Use functional components
function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null);
  
  const handleClick = () => {
    // Handler logic
  };
  
  return (
    <div>
      {/* JSX */}
    </div>
  );
}

export default MyComponent;
```

### Python/Flask

```python
# Follow PEP 8
def process_image(image, method='gradient'):
    """Process image with specified method.
    
    Args:
        image: Input image
        method: Processing method
        
    Returns:
        Processed image
    """
    # Implementation
    return result
```

## Dependency Management

### Frontend Dependencies

```json
{
  "react": "Latest stable",
  "react-dom": "Latest stable",
  "axios": "For HTTP requests"
}
```

### Backend Dependencies

```
Flask: Web framework
opencv-python: Image processing
numpy: Numerical computations
Pillow: Image manipulation
flask-cors: CORS support
```

## Version Control

### Commit Messages

```
feat: Add new feature description
fix: Fix bug description
docs: Update documentation
style: Code style changes
refactor: Code refactoring
perf: Performance improvements
test: Add tests
chore: Maintenance tasks
```

### Branch Strategy

```
main: Production-ready code
develop: Development branch
feature/feature-name: Feature branches
bugfix/bug-name: Bug fix branches
```

## Deployment Checklist

- [ ] All tests pass
- [ ] Code linting passes
- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] Dependencies updated
- [ ] Build successful
- [ ] Docker images built
- [ ] Performance tested
- [ ] Security review completed
- [ ] Documentation updated

## Troubleshooting Guide

### Common Issues

1. **OpenCV.js not loading**
   - Check CDN URL in index.html
   - Verify internet connection
   - Check browser console for CORS errors

2. **CORS errors from backend**
   - Ensure flask-cors is installed
   - Verify CORS headers in Flask app
   - Check API URL in React .env

3. **Memory leak with OpenCV objects**
   - Always call `.delete()` on Mat objects
   - Use try-finally for cleanup
   - Monitor browser memory usage

4. **Slow image processing**
   - Reduce image resolution
   - Use simpler processing method (Gradient > Sobel > Canny)
   - Check browser resource usage

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

## Resources

- [React Documentation](https://react.dev)
- [OpenCV.js Tutorials](https://docs.opencv.org/4.5.2/)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Computer Vision Fundamentals](https://en.wikipedia.org/wiki/Computer_vision)

---

Last Updated: 2024
