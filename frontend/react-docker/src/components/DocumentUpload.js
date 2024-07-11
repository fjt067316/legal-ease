import React, { useState } from "react";

function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [validationResult, setValidationResult] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:3001/api/validateLease", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => setValidationResult(data.details))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload and Validate Lease</button>
      <p>{validationResult}</p>
    </div>
  );
}

export default DocumentUpload;
