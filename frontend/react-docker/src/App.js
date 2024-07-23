import React, { useState } from "react";
import "./App.css";
import DocumentUpload from "./components/DocumentUpload";
import QueryInput from "./components/QueryInput";
import ResultDisplay from "./components/ResultDisplay";
import GenerateApiKey from "./components/GenerateApiKey";
import LogQuery from "./components/LogQuery";
import Feedback from "./components/Feedback";
import Header from "./components/Header";

function App() {
  const [apiResponse, setApiResponse] = useState("");

  const handleStatusCheck = () => {
    fetch("http://localhost:8000/api/status")
      .then((response) => response.json())
      .then((data) => setApiResponse(data.status))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="App">
      <Header />
      <button onClick={handleStatusCheck}>Check Backend Status</button>
      <p>{apiResponse}</p>
      <div className = "container">
        <GenerateApiKey />
        <DocumentUpload />
        <QueryInput />
        <ResultDisplay result = ""/>
        <LogQuery />
        <Feedback />
      </div>
    </div>
  );
}

export default App;
