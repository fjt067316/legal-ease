import React, { useState } from "react";

function Feedback() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleFeedback = () => {
    fetch("http://localhost:8000/api/feedback", {
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
    <div>
      <h2>Feedback</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter feedback"
      />
      <button onClick={handleFeedback}>Submit Feedback</button>
      <p>{response}</p>
    </div>
  );
}

export default Feedback;
