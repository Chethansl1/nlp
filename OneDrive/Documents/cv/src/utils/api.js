const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const processImageWithBackend = async (imageSource, options) => {
  try {
    const response = await fetch(`${API_URL}/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image: imageSource,
        method: options.method,
        showGradientMagnitude: options.showGradientMagnitude,
        showGradientDirection: options.showGradientDirection,
        highlightLanes: options.highlightLanes,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || 'Processing failed');
    }

    return data.processedImage;
  } catch (error) {
    console.error('Backend processing error:', error);
    throw error;
  }
};

export const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};
