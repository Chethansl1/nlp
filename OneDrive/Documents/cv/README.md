# Autonomous Vehicle Lane Detection

A comprehensive React.js web application for autonomous vehicle lane detection using gradient computation, edge detection, and OpenCV.js.

## Features

- **Image Upload**: Upload vehicle/road images for processing
- **Gradient Computation**: Compute gradient magnitude and direction using OpenCV.js
- **Multiple Edge Detection Methods**:
  - Gradient-based detection (default)
  - Sobel edge detection
  - Canny edge detection
- **Lane Highlighting**: Automatic highlighting of lane markings and vehicle edges
- **Real-time Processing**: Fast image processing in the browser
- **Discussion Points**: Comprehensive explanation of gradient computation importance in autonomous driving
- **Flask Backend**: Optional backend for flexible image processing

## Project Structure

```
cv/
├── src/
│   ├── components/
│   │   ├── ImageUpload.js
│   │   ├── ProcessedImage.js
│   │   └── DiscussionPoints.js
│   ├── utils/
│   │   └── imageProcessing.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── public/
│   └── index.html
├── backend/
│   ├── app.py
│   └── requirements.txt
├── package.json
└── README.md
```

## Installation

### Frontend Setup

1. **Install Node.js** (if not already installed)
   - Download from [nodejs.org](https://nodejs.org/)

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start the React Development Server**
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

### Backend Setup (Optional)

1. **Install Python** (if not already installed)
   - Download from [python.org](https://python.org/)

2. **Create a Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask Server**
   ```bash
   python app.py
   ```
   The server will run at `http://localhost:5000`

## Usage

1. **Upload an Image**: Click the "Upload Image" button and select a vehicle or road image
2. **Choose Detection Method**: Select from Gradient, Sobel, or Canny
3. **Configure Options**:
   - Enable/disable gradient magnitude display
   - Enable/disable gradient direction display
   - Toggle lane highlighting
4. **Process Image**: Click "Process Image" button
5. **View Results**: Switch between original and processed images using tabs
6. **Read Discussion**: Explore the discussion points section to learn about gradient computation

## OpenCV.js Integration

The application uses OpenCV.js loaded from the CDN:
```html
<script async src="https://docs.opencv.org/4.5.2/opencv.js"></script>
```

### Key Processing Functions

- **Gradient Computation**: Computes gradient magnitude and direction using Sobel operators
- **Sobel Edge Detection**: Detects edges using Sobel filters
- **Canny Edge Detection**: Advanced edge detection with noise reduction and hysteresis
- **Lane Highlighting**: Identifies and highlights lane markings using contour detection

## Technologies Used

### Frontend
- **React 18.2.0**: UI framework
- **OpenCV.js 4.5.2**: Image processing in browser
- **CSS3**: Modern styling with gradients and animations

### Backend
- **Flask 2.3.0**: Python web framework
- **OpenCV (cv2) 4.7.0**: Advanced image processing
- **Pillow 9.5.0**: Image manipulation
- **Flask-CORS 4.0.0**: Cross-origin requests support

## How Gradient Computation Works

1. **Convert to Grayscale**: Convert RGB image to grayscale
2. **Compute Gradients**: Use Sobel operators to compute:
   - Gradient X (horizontal changes)
   - Gradient Y (vertical changes)
3. **Calculate Magnitude**: `magnitude = √(Gx² + Gy²)`
4. **Calculate Direction**: `direction = arctan(Gy/Gx)`
5. **Threshold & Display**: Apply threshold and morphological operations to highlight features

## Discussion Points

The application includes detailed discussion about:
- Importance of gradient computation in autonomous driving
- Feature detection for lane following
- Obstacle detection and boundary identification
- Comparison of Sobel vs Canny edge detection
- Robustness in variable lighting conditions
- Real-time processing requirements

## API Endpoints (Backend)

### Process Image
- **Endpoint**: `POST /process`
- **Request Body**:
  ```json
  {
    "image": "base64_encoded_image",
    "method": "gradient|sobel|canny",
    "showGradientMagnitude": true,
    "showGradientDirection": false,
    "highlightLanes": true
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "processedImage": "base64_encoded_image",
    "method": "selected_method"
  }
  ```

### Health Check
- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy"}`

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

OpenCV.js requires WebAssembly support.

## Performance Tips

1. Use images up to 1920x1080 for optimal performance
2. Enable hardware acceleration in browser settings
3. Close unnecessary browser tabs
4. Use Gradient method for fastest processing
5. Canny detection is slower but produces better results

## Troubleshooting

### OpenCV.js Not Loading
- Check internet connection (CDN dependency)
- Wait a few seconds after page load for OpenCV to initialize
- Check browser console for errors

### Image Processing Fails
- Ensure image is in supported format (JPG, PNG, BMP, WebP)
- Try a smaller image
- Check browser console for specific error messages

### Flask Backend Issues
- Ensure port 5000 is available
- Verify all Python dependencies are installed
- Check that Flask server is running before using backend features

## Future Enhancements

- Real-time video processing from webcam
- Multiple region-of-interest (ROI) selection
- Advanced lane tracking algorithms
- 3D visualization of detected lanes
- Machine learning-based lane classification
- GPU acceleration for faster processing

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Note**: This application is designed for educational purposes and autonomous vehicle research. Always conduct thorough testing before deploying in production autonomous systems.
