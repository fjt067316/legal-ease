import React, { useState } from "react";

function QueryInput() {
  const [query, setQuery] = useState("");
  const [queryResponse, setQueryResponse] = useState("");

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleQuerySubmit = () => {
    fetch("http://localhost:3001/api/userQuery", {
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
    <div>
      <input type="text" value={query} onChange={handleInputChange} />
      <button onClick={handleQuerySubmit}>Submit Query</button>
      <p>{queryResponse}</p>
    </div>
  );
}

export default QueryInput;
