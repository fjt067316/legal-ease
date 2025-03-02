import React, { useState, useEffect } from "react";
import "../App.css";
import ResultDisplay from "./ResultDisplay";

const placeholderTexts = [
  "Can I bring a pet into my apartment?",
  "Can my landlord increase rent?",
  "What are my rights if I get evicted?",
  "How do I break my lease?",
  "What is the maximum security deposit?",
  "Can I sublet my apartment?",
  "What are the landlord's responsibilities?",
  "Can I withhold rent?",
];

function QueryInput() {
  const [query, setQuery] = useState("");
  const [queryResponse, setQueryResponse] = useState("");
  // const [citations, setCitations] = useState([]); // State for citations
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const [placeholder, setPlaceholder] = useState("");
  const [index, setIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const currentText = placeholderTexts[index];
    
    const timer = setTimeout(() => {
      if (!deleting) {
        if (charIndex < currentText.length) {
          setPlaceholder((prev) => prev + currentText[charIndex]);
          setCharIndex(charIndex + 1);
        } else {
          setTimeout(() => setDeleting(true), 1000); // Wait before deleting
        }
      } else {
        if (charIndex > 0) {
          setPlaceholder((prev) => prev.slice(0, -1));
          setCharIndex(charIndex - 1);
        } else {
          setDeleting(false);
          setIndex((prev) => (prev + 1) % placeholderTexts.length); // Move to next text
        }
      }
    }, deleting ? 50 : 100); // Speed up deletion

    return () => clearTimeout(timer);
  }, [charIndex, deleting, index]);

  const tryAgain = () => {
    setQuery("");
    setQueryResponse("");
    // setCitations([]);
  };
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
        // setCitations(data.citations);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setQueryResponse("An error occurred. Please try again.");
        setIsLoading(false);
      });
  };

  return (
    <div className="container-query">

      {
        !isLoading && queryResponse == "" &&
      <div className="section">
        <h2>Ask a Question</h2>
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          className="input"
          placeholder={query ? "" : placeholder}
        />
        <button onClick={handleQuerySubmit} className="button" disabled={isLoading}>
          {isLoading ? "Processing..." : "Submit Query"}
        </button>
      </div>
      }
      { (isLoading || queryResponse != "") &&
        <div className="section-results">
        {isLoading ? <p>Loading...</p> : <ResultDisplay result={queryResponse} />}
        <button onClick={tryAgain} className="button" disabled={isLoading}>
          {isLoading ? "Processing..." : "Try again"}
        </button>
      </div>
      }
    </div>
  );
}

export default QueryInput;
