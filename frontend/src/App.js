// src/App.js
import React, { useState } from 'react';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [colorCount, setColorCount] = useState(1);
  const [imageCount, setImageCount] = useState(4);
  const [colors, setColors] = useState(['#ffffff']);

  // Handle file selection
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files); // Convert FileList to Array
    setSelectedFiles(files);
  };

  // Handles color count change
  // const handleColorCountChange = (event) => {
  //   setColorCount(event.target.value);
  // };

  const handleImageCountChange = (event) => {
    setImageCount(event.target.value);
  };

  const handleColorCountChange = (e) => {
    const count = parseInt(e.target.value, 10);
    setColorCount(count);
    setColors(Array(count).fill('#ffffff'));
  };

  const handleColorChange = (index, newColor) => {
    const updatedColors = [...colors];
    updatedColors[index] = newColor;
    setColors(updatedColors);
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
    formData.append('imageCount', imageCount);

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



    const handleGetCollage = async () => {
      const formData = new FormData();
      formData.append('imageCount', imageCount);
      formData.append('colors', colors);

      try {
      const response = await fetch('http://127.0.0.1:5000/create', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        alert("Collage created successfully");
      } else {
        alert("Collage creation failed");
      }
    } catch (error) {
      console.error('Error creating collage:', error);
      alert("Collage creation failed");
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

        <div>
          {colors.map((color, index) => (
              <div key={index} style={{margin: '10px 0'}}>
                <label>Color {index + 1}: </label>
                <input
                    type="color"
                    value={color}
                    onChange={(e) => handleColorChange(index, e.target.value)}
                />
              </div>
          ))}
        </div>

        <div style={{margin: '20px 0'}}>
          <label>Select number of images in the collage: </label>
          <select value={imageCount} onChange={handleImageCountChange}>
            <option value="4">4 Images</option>
            <option value="9">9 Images</option>
            <option value="16">16 Images</option>
            <option value="25">25 Images</option>
          </select>
        </div>


        <button onClick={handleFileUpload}>Upload Files</button>

        <button onClick={handleGetCollage} style={{margin: '10px'}}>
          Get Collage
        </button>
      </div>
  );
}

export default App;
