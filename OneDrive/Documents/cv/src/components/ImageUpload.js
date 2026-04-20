import React, { useRef } from 'react';

function ImageUpload({ onImageUpload }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        return;
      }
      onImageUpload(file);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-input-wrapper">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
      />
      <button className="file-input-button" onClick={handleButtonClick}>
        📷 Upload Image
      </button>
      <p style={{ marginTop: '10px', color: '#999', fontSize: '0.85em' }}>
        Supported formats: JPG, PNG, BMP, WebP
      </p>
    </div>
  );
}

export default ImageUpload;
