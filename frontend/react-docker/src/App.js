import React, { useState } from "react";
import "./App.css";
import DocumentUpload from "./components/DocumentUpload";
import QueryInput from "./components/QueryInput";
import ResultDisplay from "./components/ResultDisplay";
import GenerateApiKey from "./components/GenerateApiKey";

function App() {
  const [apiResponse, setApiResponse] = useState("");
  const [result, setResult] = useState("");

  const handleStatusCheck = () => {
    fetch("http://localhost:3001/api/status")
      .then((response) => response.json())
      .then((data) => setApiResponse(data.status))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="App">
      <button onClick={handleStatusCheck}>Check Backend Status</button>
      <p>{apiResponse}</p>
      <GenerateApiKey />
      <DocumentUpload />
      <QueryInput />
      <ResultDisplay result={result} />
    </div>
  );
}

export default App;
