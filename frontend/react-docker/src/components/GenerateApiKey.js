import React, { useState } from "react";

function GenerateApiKey() {
  const [apiKey, setApiKey] = useState("");

  const handleGenerateApiKey = () => {
    fetch("http://localhost:3001/api/generate-api-key")
      .then((response) => response.json())
      .then((data) => setApiKey(data.apiKey))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div>
      <button onClick={handleGenerateApiKey}>Generate API Key</button>
      <p>{apiKey}</p>
    </div>
  );
}

export default GenerateApiKey;
