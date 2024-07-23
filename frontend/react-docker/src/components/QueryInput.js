import React, { useState } from "react";
import "../App.css";

function QueryInput() {
  const [query, setQuery] = useState("");
  const [queryResponse, setQueryResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleQuerySubmit = () => {
    setIsLoading(true); // Set loading to true when starting the fetch
    fetch("http://localhost:8000/api/userQuery", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    })
      .then((response) => response.json())
      .then((data) => {
        setQueryResponse(data.response);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setIsLoading(false);
      });
  };

  return (
    <div className="section">
      <h2>Submit Query</h2>
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        className="input"
      />
      <button
        onClick={handleQuerySubmit}
        className="button"
        disabled={isLoading}
      >
        {isLoading ? "processing..." : "Submit Query"}
      </button>
      <p>{queryResponse}</p>
    </div>
  );
}

export default QueryInput;
