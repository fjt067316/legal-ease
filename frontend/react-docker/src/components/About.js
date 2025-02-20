import React from "react";
import "../App.css";
import TeamImage from "../group-62-photo.png"; // Update with actual image path

const aboutText = [
  "We",
  "are",
  "a",
  "team",
  "of",
  "students",
  "passionate",
  "about",
  "access",
  "to",
  "legal",
  "information.",
  "LegalEase",
  "was",
  "built",
  "to",
  "help",
  "students",
  "understand",
  "their",
  "housing",
  "rights",
  "without",
  "costly",
  "legal",
  "consultations.",
];

function About() {
  return (
    <div className="about-container">
      <img src={TeamImage} alt="Our Team" className="team-image" />
      <div className="about-text">
      <p className="fade-in-words">
        {aboutText.map((word, index) => (
          <span key={index} className="word" style={{ animationDelay: `${index * 0.3}s` }}>
            {word}{" "}
          </span>
        ))}
      </p>
      </div>
    </div>
  );
}

export default About;
