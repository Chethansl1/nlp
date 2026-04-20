from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os
import sys

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def base64_to_image(base64_str):
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def image_to_base64(image):
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode()
    return f"data:image/png;base64,{image_base64}"


def compute_gradient(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = np.uint8(255 * magnitude / np.max(magnitude))
    
    direction = np.arctan2(grad_y, grad_x) * (180 / np.pi)
    
    return magnitude, direction


def compute_sobel(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    
    _, threshold = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)
    
    return threshold


def compute_canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edges = cv2.Canny(blurred, 50, 150)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    return dilated


def highlight_lane_markings(image, magnitude):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    _, binary = cv2.threshold(normalized, 100, 255, cv2.THRESH_BINARY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    display = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < gray.shape[0] * gray.shape[1] * 0.5:
            cv2.drawContours(display, [contour], 0, (0, 255, 0), 2)
    
    return display


@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        base64_image = data.get('image')
        method = data.get('method', 'gradient')
        show_magnitude = data.get('showGradientMagnitude', True)
        show_direction = data.get('showGradientDirection', False)
        highlight_lanes = data.get('highlightLanes', True)
        
        if not base64_image:
            return jsonify({'error': 'No image provided'}), 400
        
        image = base64_to_image(base64_image)
        
        if method == 'gradient':
            magnitude, direction = compute_gradient(image)
            if show_magnitude and highlight_lanes:
                result = highlight_lane_markings(image, magnitude)
            elif show_magnitude:
                result = magnitude
            elif show_direction:
                result = np.uint8(direction)
            else:
                result = magnitude
        
        elif method == 'sobel':
            result = compute_sobel(image)
        
        elif method == 'canny':
            result = compute_canny(image)
        
        else:
            return jsonify({'error': 'Unknown method'}), 400
        
        result_base64 = image_to_base64(result)
        
        return jsonify({
            'success': True,
            'processedImage': result_base64,
            'method': method
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Lane Detection Backend Server")
    print("="*50)
    print("Starting Flask server...")
    print("Backend URL: http://localhost:5000")
    print("Health Check: http://localhost:5000/health")
    print("="*50 + "\n")
    sys.stdout.flush()
    app.run(debug=False, port=5000, host='0.0.0.0')
