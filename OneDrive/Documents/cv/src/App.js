import React, { useState, useRef, useEffect } from 'react';
import ImageUpload from './components/ImageUpload';
import ProcessedImage from './components/ProcessedImage';
import DiscussionPoints from './components/DiscussionPoints';
import { processImageWithOpenCV } from './utils/imageProcessing';
import { processImageWithBackend, checkBackendHealth } from './utils/api';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [edgeDetectionMethod, setEdgeDetectionMethod] = useState('gradient');
  const [showGradientMagnitude, setShowGradientMagnitude] = useState(true);
  const [showGradientDirection, setShowGradientDirection] = useState(false);
  const [highlightLanes, setHighlightLanes] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [processedImageType, setProcessedImageType] = useState('original');
  const [backendAvailable, setBackendAvailable] = useState(false);

  useEffect(() => {
    checkBackendHealth().then(setBackendAvailable);
  }, []);

  const handleImageUpload = (file) => {
    setError(null);
    const reader = new FileReader();
    reader.onload = (e) => {
      setOriginalImage(e.target.result);
      setProcessedImage(null);
      setProcessedImageType('original');
    };
    reader.readAsDataURL(file);
  };

  const handleProcessImage = async () => {
    if (!originalImage) {
      setError('Please upload an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let result;

      if (backendAvailable) {
        result = await processImageWithBackend(originalImage, {
          method: edgeDetectionMethod,
          showGradientMagnitude,
          showGradientDirection,
          highlightLanes,
        });
      } else {
        result = await processImageWithOpenCV(originalImage, {
          method: edgeDetectionMethod,
          showGradientMagnitude,
          showGradientDirection,
          highlightLanes,
        });
      }

      setProcessedImage(result);
      setProcessedImageType(edgeDetectionMethod);
    } catch (err) {
      setError(`Error processing image: ${err.message}`);
      console.error('Image processing error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>🚗 Autonomous Vehicle Lane Detection</h1>
        <p>Advanced edge detection for lane marking and obstacle identification</p>
        <p style={{ fontSize: '0.85em', marginTop: '10px', opacity: 0.8 }}>
          {backendAvailable ? '✅ Backend Connected' : '📡 Using Browser Processing'}
        </p>
      </div>

      <div className="main-container">
        <div className="panel upload-panel">
          <div className="upload-section">
            <h2>Image Upload & Controls</h2>
            <ImageUpload onImageUpload={handleImageUpload} />
          </div>

          <div className="controls">
            <div className="control-group">
              <label>Edge Detection Method:</label>
              <select
                value={edgeDetectionMethod}
                onChange={(e) => setEdgeDetectionMethod(e.target.value)}
              >
                <option value="gradient">Gradient (Default)</option>
                <option value="sobel">Sobel Edge Detection</option>
                <option value="canny">Canny Edge Detection</option>
              </select>
            </div>

            <div className="control-group">
              <label>
                <input
                  type="checkbox"
                  checked={showGradientMagnitude}
                  onChange={(e) => setShowGradientMagnitude(e.target.checked)}
                />
                {' '}Show Gradient Magnitude
              </label>
            </div>

            <div className="control-group">
              <label>
                <input
                  type="checkbox"
                  checked={showGradientDirection}
                  onChange={(e) => setShowGradientDirection(e.target.checked)}
                />
                {' '}Show Gradient Direction
              </label>
            </div>

            <div className="control-group">
              <label>
                <input
                  type="checkbox"
                  checked={highlightLanes}
                  onChange={(e) => setHighlightLanes(e.target.checked)}
                />
                {' '}Highlight Lane Markings
              </label>
            </div>

            <button
              className="process-button"
              onClick={handleProcessImage}
              disabled={!originalImage || loading}
            >
              {loading ? 'Processing...' : 'Process Image'}
            </button>

            {error && <div className="error-message">{error}</div>}
          </div>
        </div>

        <div className="panel display-panel">
          <h2>Image Display</h2>
          <ProcessedImage
            originalImage={originalImage}
            processedImage={processedImage}
            currentType={processedImageType}
            onTypeChange={setProcessedImageType}
          />
        </div>
      </div>

      <div className="discussion-panel">
        <DiscussionPoints />
      </div>

      <div className="footer">
        <p>© 2024 Autonomous Vehicle Lane Detection System | Powered by React & OpenCV.js</p>
      </div>
    </div>
  );
}

export default App;
