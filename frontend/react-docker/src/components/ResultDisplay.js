import React from "react";
import "../App.css";


function ResultDisplay({ result, citations }) {
  return (
    <div>
      <h2>Answer:</h2>
      <p>{result}</p>
      <h2>Citations:</h2>
      <ul>
        {citations.map((citation, index) => (
          <li key={index}>{`${index + 1}. ${citation}`}</li>
        ))}
      </ul>
    </div>
  );
}

export default ResultDisplay;
