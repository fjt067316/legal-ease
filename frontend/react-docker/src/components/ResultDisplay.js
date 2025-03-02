import React from "react";
import "../App.css";


function ResultDisplay({ result, query, citations }) {
  return (
    <div>
      <h2>{query}:</h2>
      <p>{result}</p>
      {/* <p>{citations}</p> */}
      <h2>Citations:</h2>
      <ul>
  {Array.isArray(citations) && citations.length > 0 ? (
    citations.map((citation, index) => (
      <li key={index}>{`${index + 1}. ${citation}`}</li>
    ))
  ) : (
    <li>No citations available</li>
  )}
</ul>
    </div>
  );
}

export default ResultDisplay;
