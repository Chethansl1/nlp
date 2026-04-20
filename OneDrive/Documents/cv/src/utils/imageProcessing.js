export const processImageWithOpenCV = async (imageSource, options) => {
  return new Promise((resolve, reject) => {
    if (typeof cv === 'undefined') {
      reject(new Error('OpenCV.js not loaded'));
      return;
    }

    try {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        let src = cv.imread(canvas);
        let dst;

        if (options.method === 'gradient') {
          dst = computeGradient(src, options);
        } else if (options.method === 'sobel') {
          dst = computeSobel(src);
        } else if (options.method === 'canny') {
          dst = computeCanny(src);
        }

        if (dst) {
          cv.imshow(canvas, dst);
          const processedImage = canvas.toDataURL('image/png');
          resolve(processedImage);

          src.delete();
          dst.delete();
        }
      };

      img.onerror = () => reject(new Error('Failed to load image'));
      img.src = imageSource;
    } catch (error) {
      reject(error);
    }
  });
};

function computeGradient(src, options) {
  const gray = new cv.Mat();
  const gradX = new cv.Mat();
  const gradY = new cv.Mat();
  const gradMagnitude = new cv.Mat();

  cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);

  const kernel = cv.getStructuringElement(cv.MORPH_RECT, new cv.Size(3, 3));

  cv.Sobel(gray, gradX, cv.CV_32F, 1, 0, 3);
  cv.Sobel(gray, gradY, cv.CV_32F, 0, 1, 3);

  cv.magnitude(gradX, gradY, gradMagnitude);

  let display;
  if (options.showGradientMagnitude && options.highlightLanes) {
    display = highlightLaneMarkings(gradMagnitude, gray);
  } else if (options.showGradientMagnitude) {
    display = normalizeAndConvert(gradMagnitude);
  } else {
    display = normalizeAndConvert(gradMagnitude);
  }

  gray.delete();
  gradX.delete();
  gradY.delete();
  gradMagnitude.delete();
  kernel.delete();

  return display;
}

function computeSobel(src) {
  const gray = new cv.Mat();
  const gradX = new cv.Mat();
  const gradY = new cv.Mat();
  const absgradX = new cv.Mat();
  const absgradY = new cv.Mat();
  const dst = new cv.Mat();

  cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);
  cv.Sobel(gray, gradX, cv.CV_32F, 1, 0, 3);
  cv.Sobel(gray, gradY, cv.CV_32F, 0, 1, 3);

  gradX.convertTo(absgradX, cv.CV_8U);
  gradY.convertTo(absgradY, cv.CV_8U);

  cv.addWeighted(absgradX, 0.5, absgradY, 0.5, 0, dst);

  const threshold = cv.Mat.zeros(dst.rows, dst.cols, cv.CV_8U);
  cv.threshold(dst, threshold, 50, 255, cv.THRESH_BINARY);

  gray.delete();
  gradX.delete();
  gradY.delete();
  absgradX.delete();
  absgradY.delete();
  dst.delete();

  return threshold;
}

function computeCanny(src) {
  const gray = new cv.Mat();
  const edges = new cv.Mat();

  cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);

  cv.GaussianBlur(gray, gray, new cv.Size(5, 5), 0);

  cv.Canny(gray, edges, 50, 150);

  const dilated = new cv.Mat();
  const kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, new cv.Size(3, 3));
  cv.dilate(edges, dilated, kernel, new cv.Point(-1, -1), 2);

  gray.delete();
  edges.delete();
  kernel.delete();

  return dilated;
}

function normalizeAndConvert(src) {
  const normalized = new cv.Mat();
  const display = new cv.Mat();

  cv.normalize(src, normalized, 0, 255, cv.NORM_MINMAX);
  normalized.convertTo(display, cv.CV_8U);

  normalized.delete();

  return display;
}

function highlightLaneMarkings(gradMagnitude, gray) {
  const normalized = new cv.Mat();
  const binary = new cv.Mat();
  const display = new cv.Mat();

  cv.normalize(gradMagnitude, normalized, 0, 255, cv.NORM_MINMAX);
  normalized.convertTo(normalized, cv.CV_8U);

  cv.threshold(normalized, binary, 100, 255, cv.THRESH_BINARY);

  const kernel = cv.getStructuringElement(cv.MORPH_RECT, new cv.Size(3, 3));
  cv.morphologyEx(binary, binary, cv.MORPH_CLOSE, kernel);

  const lines = cv.Mat.zeros(gray.rows, gray.cols, cv.CV_8UC3);
  cv.cvtColor(binary, display, cv.COLOR_GRAY2BGR);

  const contours = new cv.MatVector();
  const hierarchy = new cv.Mat();

  const temp = binary.clone();
  cv.findContours(temp, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);

  for (let i = 0; i < contours.size(); i++) {
    const contour = contours.get(i);
    const area = cv.contourArea(contour);

    if (area > 100 && area < gray.rows * gray.cols * 0.5) {
      cv.drawContours(display, contours, i, new cv.Scalar(0, 255, 0), 2);
    }

    contour.delete();
  }

  normalized.delete();
  binary.delete();
  lines.delete();
  kernel.delete();
  contours.delete();
  hierarchy.delete();
  temp.delete();

  return display;
}
