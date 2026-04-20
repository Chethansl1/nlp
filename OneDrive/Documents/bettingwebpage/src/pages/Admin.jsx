import React, { useState } from 'react';

const Admin = () => {
  const [file, setFile] = useState(null);
  const [previewData, setPreviewData] = useState([]);
  const [columnMapping, setColumnMapping] = useState({
    date: '',
    title: '',
    summary: '',
    source: '',
    url: '',
    tags: ''
  });

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);

    // Simulate CSV parsing - in real app use papaparse or similar
    if (uploadedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        const lines = text.split('\n').slice(0, 6); // First 5 rows + header
        const parsed = lines.map(line => line.split(','));
        setPreviewData(parsed);
      };
      reader.readAsText(uploadedFile);
    }
  };

  const handleMappingChange = (field, value) => {
    setColumnMapping(prev => ({ ...prev, [field]: value }));
  };

  const handleIngest = () => {
    // In real app, send data to backend API
    alert('Data ingested successfully! (This is a demo)');
  };

  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-text mb-8 text-center">Data Administration</h1>

        <div className="bg-white p-8 rounded-2xl shadow-lg mb-8">
          <h2 className="text-2xl font-semibold text-text mb-6">Upload News Data</h2>

          <div className="mb-6">
            <label className="block text-text font-medium mb-2">Select File (CSV/JSON/HDF5)</label>
            <input
              type="file"
              accept=".csv,.json,.hdf5"
              onChange={handleFileUpload}
              className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {previewData.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-text mb-4">Data Preview (First 5 rows)</h3>
              <div className="overflow-x-auto bg-gray-50 p-4 rounded-xl">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      {previewData[0]?.map((header, index) => (
                        <th key={index} className="text-left p-2 font-medium">{header}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {previewData.slice(1).map((row, rowIndex) => (
                      <tr key={rowIndex} className="border-b border-gray-200">
                        {row.map((cell, cellIndex) => (
                          <td key={cellIndex} className="p-2">{cell}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {previewData.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-text mb-4">Column Mapping</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.keys(columnMapping).map(field => (
                  <div key={field}>
                    <label className="block text-text font-medium mb-2 capitalize">{field}</label>
                    <select
                      value={columnMapping[field]}
                      onChange={(e) => handleMappingChange(field, e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="">Select column...</option>
                      {previewData[0]?.map((header, index) => (
                        <option key={index} value={header}>{header}</option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={handleIngest}
            disabled={!file}
            className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Confirm & Ingest Data
          </button>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold text-text mb-6">Alternative: Ingest from URL</h2>

          <div className="mb-4">
            <label className="block text-text font-medium mb-2">RSS/NewsAPI URL</label>
            <input
              type="url"
              placeholder="https://api.example.com/news/rss"
              className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div className="mb-6">
            <label className="block text-text font-medium mb-2">API Key (if required)</label>
            <input
              type="password"
              placeholder="Enter API key..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <button className="w-full bg-accent text-white py-3 rounded-xl font-semibold hover:bg-accent/90 transition-colors">
            Fetch & Process News
          </button>

          <div className="mt-4 p-4 bg-blue-50 rounded-xl">
            <p className="text-blue-800 text-sm">
              <strong>Example URLs:</strong><br />
              NewsAPI: https://newsapi.org/v2/everything?q=betting+india&apiKey=YOUR_KEY<br />
              RSS: https://indianexpress.com/section/cities/delhi/feed/
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admin;