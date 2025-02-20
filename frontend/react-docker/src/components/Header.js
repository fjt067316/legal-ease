import React from "react";
import "../App.css";

function Header() {
  return (
    <div className="header">
      <p className="fade-in-words">
  {[
    "LegalEase",
    "simplifies",
    "housing",
    "rights",
    "by",
    "providing",
    "quick",
    "and",
    "reliable",
    "answers",
    "to",
    "students.",
    "No",
    "need",
    "for",
    "costly",
    "consultations.",
    "Transparent",
    "citations",
    "empower",
    "users",
    "to",
    "verify",
    "information.",
  ].map((word, index) => (
    <span key={index} className="word" style={{ animationDelay: `${index * 0.3}s` }}>
      {word}{" "}
    </span>
  ))}
</p>
    </div>
  );
}

export default Header;
