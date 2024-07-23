import React, { useState } from "react";
import "../App.css";

function QueryInput() {
  const [query, setQuery] = useState("");
  const [queryResponse, setQueryResponse] = useState("");

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleQuerySubmit = () => {
    fetch("http://localhost:8000/api/userQuery", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    })
      .then((response) => response.json())
      .then((data) => setQueryResponse(data.response))
      .catch((error) => console.error("Error:", error));
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
      <button onClick={handleQuerySubmit} className="button">
        Submit Query
      </button>
      <p>{queryResponse}</p>
    </div>
  );
}

export default QueryInput;
