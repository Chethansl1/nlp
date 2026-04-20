import React from 'react';

function ProcessedImage({ originalImage, processedImage, currentType, onTypeChange }) {
  return (
    <div className="image-display-section">
      {originalImage && (
        <div>
          <div className="tab-buttons">
            <button
              className={`tab-button ${currentType === 'original' ? 'active' : ''}`}
              onClick={() => onTypeChange('original')}
            >
              Original
            </button>
            {processedImage && (
              <>
                <button
                  className={`tab-button ${currentType === 'gradient' ? 'active' : ''}`}
                  onClick={() => onTypeChange('gradient')}
                >
                  Gradient
                </button>
                <button
                  className={`tab-button ${currentType === 'sobel' ? 'active' : ''}`}
                  onClick={() => onTypeChange('sobel')}
                >
                  Sobel
                </button>
                <button
                  className={`tab-button ${currentType === 'canny' ? 'active' : ''}`}
                  onClick={() => onTypeChange('canny')}
                >
                  Canny
                </button>
              </>
            )}
          </div>

          <div className="image-container">
            {currentType === 'original' && (
              <img src={originalImage} alt="Original" />
            )}
            {processedImage && currentType !== 'original' && (
              <img src={processedImage} alt="Processed" />
            )}
          </div>

          {processedImage && (
            <div className="processing-info">
              <p>
                <strong>Processing Info:</strong> Image processed with edge detection.
                Gradient computation identifies pixel intensity changes for lane and edge detection.
              </p>
            </div>
          )}
        </div>
      )}
      {!originalImage && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
          <p>Upload an image to see the processing results here</p>
        </div>
      )}
    </div>
  );
}

export default ProcessedImage;
