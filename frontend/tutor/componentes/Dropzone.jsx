"use client";

import React, { useState, useRef } from 'react';
import './Dropzone.module.css'; 

function Dropzone() {
  const [files, setFiles] = useState([]);
  const dropzoneRef = useRef(null);

  const handleDragOver = (event) => {
    event.preventDefault();
    dropzoneRef.current.classList.add('dropzone-active');
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    dropzoneRef.current.classList.remove('dropzone-active');
  };

  const handleDrop = (event) => {
    event.preventDefault();
    dropzoneRef.current.classList.remove('dropzone-active');

    const newFiles = Array.from(event.dataTransfer.files);
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleFileSelect = (event) => {
    const newFiles = Array.from(event.target.files);
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleRemoveFile = (index) => {
    const updatedFiles = [...files];
    updatedFiles.splice(index, 1);
    setFiles(updatedFiles);
  };

  return (
    <div
      ref={dropzoneRef}
      className="dropzone"
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <p>Arraste e solte arquivos aqui ou</p>
      <label htmlFor="fileInput" className="file-input-label">
        Selecione arquivos
      </label>
      <input
        type="file"
        id="fileInput"
        multiple
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />

      {files.length > 0 && (
        <div className="file-list">
          <h3>Arquivos Selecionados:</h3>
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                {file.name} ({formatFileSize(file.size)})
                <button onClick={() => handleRemoveFile(index)}>Remover</button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export default Dropzone;