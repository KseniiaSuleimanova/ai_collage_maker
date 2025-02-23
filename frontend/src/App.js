// src/App.js
import React, { useState } from 'react';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [colorCount, setColorCount] = useState(1);

  // Handle file selection
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files); // Convert FileList to Array
    setSelectedFiles(files);
  };

  // Handles color count change
  const handleColorCountChange = (event) => {
    setColorCount(event.target.value);
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
    formData.append('colorCount', colorCount);

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
      <div style={{textAlign: 'center', marginTop: '50px'}}>
        <input type="file" onChange={handleFileChange} accept=".jpg,.jpeg,.png" multiple/>

        <div style={{margin: '20px 0'}}>
          <label>Select number of dominant colors: </label>
          <select value={colorCount} onChange={handleColorCountChange}>
            <option value="1">1 Color</option>
            <option value="2">2 Colors</option>
            <option value="3">3 Colors</option>
            <option value="5">5 Colors</option>
          </select>
        </div>


        <button onClick={handleFileUpload}>Upload Files</button>
      </div>
  );
}

export default App;
