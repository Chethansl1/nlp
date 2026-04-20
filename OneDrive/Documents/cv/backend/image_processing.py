import cv2
import numpy as np

class LaneDetector:
    def __init__(self):
        self.min_area = 100
        self.max_area_ratio = 0.5

    def compute_gradient(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        magnitude = np.uint8(255 * magnitude / (np.max(magnitude) + 1e-5))
        
        direction = np.arctan2(grad_y, grad_x) * (180 / np.pi)
        direction = np.uint8((direction + 180) / 360 * 255)
        
        return magnitude, direction, grad_x, grad_y

    def compute_sobel_edges(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        
        sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        
        _, threshold = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)
        
        return threshold

    def compute_canny_edges(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        edges = cv2.Canny(blurred, 50, 150)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        return dilated

    def highlight_lane_markings(self, image, magnitude):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        _, binary = cv2.threshold(normalized, 100, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        display = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        lane_points = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area < area < gray.shape[0] * gray.shape[1] * self.max_area_ratio:
                cv2.drawContours(display, [contour], 0, (0, 255, 0), 2)
                lane_points.append(contour)
        
        return display, lane_points

    def detect_vehicle_edges(self, image):
        edges = self.compute_canny_edges(image)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        vehicle_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) >= 3:
                    cv2.drawContours(display, [approx], 0, (255, 0, 0), 2)
                    vehicle_contours.append(approx)
        
        return display, vehicle_contours

    def process_image(self, image, method='gradient', options=None):
        if options is None:
            options = {}
        
        if method == 'gradient':
            magnitude, direction, _, _ = self.compute_gradient(image)
            
            if options.get('highlight_lanes', True):
                result, _ = self.highlight_lane_markings(image, magnitude)
            else:
                result = magnitude
        
        elif method == 'sobel':
            result = self.compute_sobel_edges(image)
        
        elif method == 'canny':
            result = self.compute_canny_edges(image)
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return result
