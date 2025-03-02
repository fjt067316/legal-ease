import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import '../App.css';

export default function NavBar() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const navigate = useNavigate(); // Replace useHistory with useNavigate
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });

  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const handleStatusClick = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/status");
      if (response.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch (error) {
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="navbar">
      <div className="title" onClick={() => navigate('/')}>
        LegalEase
      </div>
      <div className="links">
        <span className="link" onClick={() => navigate('/')}>Home</span>
        <span className="link" onClick={() => navigate('/about')}>About</span>
        {/* <span className="link" onClick={() => navigate('/upload')}>Upload a Lease</span> */}
        <button className="statusButton" onClick={handleStatusClick} disabled={loading}>
          {loading ? "⏳" : status === "success" ? "✅" : status === "error" ? "❌" : "Check Status"}
        </button>
        <button className="dark-mode-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀️" : "🌙"}
        </button>
      </div>
    </div>
  );
}
