import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  // Handle uploading and analyzing the image via your FastAPI backend
  const handleInspect = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/inspect", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze image. Ensure the backend server is running.");
      }

      const data = await response.json();
      setResult(data.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: '40px auto', padding: '20px', textAlign: 'center' }}>
      <h1>AI Asset & Realism Inspector</h1>
      <p style={{ color: '#666' }}>Upload an AI-generated image to check for artifacts, over-smoothing, and realism scores.</p>

      {/* File Upload Box */}
      <div style={{ border: '2px dashed #ccc', padding: '30px', borderRadius: '10px', margin: '20px 0', background: '#fafafa' }}>
        <input type="file" accept="image/*" onChange={handleFileChange} style={{ marginBottom: '15px' }} />
        
        {previewUrl && (
          <div>
            <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', maxHeight: '250px', borderRadius: '8px', marginTop: '10px' }} />
          </div>
        )}
      </div>

      {/* Inspect Button */}
      <button 
        onClick={handleInspect} 
        disabled={!selectedFile || loading}
        style={{ background: '#0070f3', color: 'white', border: 'none', padding: '12px 24px', fontSize: '16px', borderRadius: '5px', cursor: 'pointer', opacity: (!selectedFile || loading) ? 0.6 : 1 }}
      >
        {loading ? "Analyzing Pixels..." : "Inspect Realism"}
      </button>

      {/* Error Message */}
      {error && <p style={{ color: 'red', marginTop: '15px' }}>{error}</p>}

      {/* Results Display */}
      {result && (
        <div style={{ marginTop: '30px', padding: '20px', background: '#f0f4f8', borderRadius: '8px', textAlign: 'left' }}>
          <h3>Analysis Report</h3>
          <p><strong>Realism Score:</strong> <span style={{ fontSize: '20px', color: '#0070f3' }}>{result.realism_score} / 100</span></p>
          
          <h4>Metrics:</h4>
          <ul>
            <li>Sharpness Index: {result.metrics.sharpness_index}</li>
            <li>Contrast Index: {result.metrics.contrast_index}</li>
          </ul>

          <h4>Diagnostic Tips:</h4>
          <ul>
            {result.tips.map((tip, index) => (
              <li key={index} style={{ marginBottom: '5px' }}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
