import React, { useState } from "react";
import "../App.css";

function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [validationResult, setValidationResult] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:8000/api/validateLease", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => setValidationResult(data.details))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="section">
      <h2>Upload File</h2>
      <input type="file" onChange={handleFileChange} className="file-input" />
      <button onClick={handleFileUpload} className="button">
        Upload and Validate Lease
      </button>
      <p>{validationResult}</p>
    </div>
  );
}

export default DocumentUpload;
