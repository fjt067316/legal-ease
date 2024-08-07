import React, { useState } from "react";
import "../App.css";


function LogQuery() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleLogQuery = () => {
    fetch("http://localhost:8000/api/log", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })
      .then((res) => res.json())
      .then((data) => setResponse(data.response))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="section">
      <h2>Log Query</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter query to log"
        className="input"
      />
      <button onClick={handleLogQuery} className="button">Log Query</button>
      <p>{response}</p>
    </div>
  );
}


export default LogQuery;
