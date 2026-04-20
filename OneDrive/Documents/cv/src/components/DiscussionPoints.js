import React from 'react';

function DiscussionPoints() {
  const points = [
    {
      title: 'Importance of Gradient Computation',
      content:
        'Gradient computation is fundamental in computer vision for detecting edges and boundaries. By calculating the rate of change in pixel intensity, gradients reveal where significant visual features (like lane markings) transition from one region to another. This is essential for identifying the structure and topology of objects in autonomous driving scenarios.',
    },
    {
      title: 'Feature Detection for Lane Following',
      content:
        'Lane markings are typically high-contrast features that produce strong gradient responses. By computing gradients, we can identify these features even under varying lighting conditions. The gradient magnitude tells us the strength of the edge, while gradient direction indicates the orientation of lane markings—critical information for steering control systems.',
    },
    {
      title: 'Obstacle Detection and Boundary Identification',
      content:
        'Vehicle edges and obstacles create distinctive gradient patterns. Computing gradients allows the system to identify the boundaries of other vehicles, road boundaries, and obstacles. This boundary information is crucial for collision avoidance and maintaining safe distance from other road users.',
    },
    {
      title: 'Sobel vs Canny Edge Detection',
      content:
        'Sobel operators provide basic edge detection through gradient computation but can be sensitive to noise. Canny edge detection builds on Sobel by applying Gaussian filtering for noise reduction, non-maximum suppression to thin edges, and hysteresis thresholding for better edge continuity. For autonomous driving, Canny typically provides cleaner lane markings.',
    },
    {
      title: 'Robustness in Variable Lighting',
      content:
        'Gradient-based methods are inherently more robust to lighting variations than simple thresholding because they capture relative intensity changes rather than absolute values. This makes them ideal for autonomous vehicles that operate in diverse environmental conditions—sunny roads, shadows, and nighttime driving.',
    },
    {
      title: 'Real-time Processing Requirements',
      content:
        'Gradient computation is computationally efficient and can be parallelized across GPU cores, making it suitable for real-time processing on embedded systems. For autonomous vehicles running on edge devices, efficient gradient computation is essential to maintain high frame rates (typically 30+ FPS) for responsive control systems.',
    },
  ];

  return (
    <div>
      <h2>💡 Discussion Points: Gradient Computation in Autonomous Driving</h2>
      <div className="discussion-points">
        {points.map((point, index) => (
          <div key={index} className="discussion-point">
            <h3>{point.title}</h3>
            <p>{point.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DiscussionPoints;
