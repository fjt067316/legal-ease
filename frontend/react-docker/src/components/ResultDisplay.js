import React from "react";
import "../App.css";


function ResultDisplay({ result }) {
  return (
    <div className="section">
      <h2>Result</h2>
      <p>{result}</p>
    </div>
  );
}

export default ResultDisplay;
