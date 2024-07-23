import React, { useState } from "react";
import "../App.css";


function GenerateApiKey() {
  const [apiKey, setApiKey] = useState("");

  const handleGenerateApiKey = () => {
    fetch("http://localhost:8000/api/generate-api-key")
      .then((response) => response.json())
      .then((data) => setApiKey(data.apiKey))
      .catch((error) => console.error("Error:", error));
  };

  return (

    <div className="section">
      <h2>Generate API Key</h2>
      <button onClick={handleGenerateApiKey} className="button">Generate API Key</button>
      <p>{apiKey}</p>
    </div>
  );
}

export default GenerateApiKey;
