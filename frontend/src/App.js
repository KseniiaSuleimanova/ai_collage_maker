// src/App.js
import React, { useState } from 'react';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);

  // Handle file selection
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files); // Convert FileList to Array
    setSelectedFiles(files);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (selectedFiles.length === 0) {
      alert("Please select at least one file to upload");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file, index) => {
      formData.append(`file${index}`, file); // Append each file with a unique key
    });

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        alert("Files uploaded successfully");
      } else {
        alert("File upload failed");
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert("File upload failed");
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <input type="file" onChange={handleFileChange} accept=".jpg,.jpeg,.png" multiple />
      <button onClick={handleFileUpload}>Upload Files</button>
    </div>
  );
}

export default App;
