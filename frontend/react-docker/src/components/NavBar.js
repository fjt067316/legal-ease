import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import '../App.css';

export default function NavBar() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const navigate = useNavigate(); // Replace useHistory with useNavigate

  const handleStatusClick = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/status"); // Ensure this matches your backend endpoint
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
        <span className="link" onClick={() => navigate('/upload')}>Upload a Lease</span>
        <button className="statusButton" onClick={handleStatusClick} disabled={loading}>
            {loading ? "⏳" : status === "success" ? "✅" : status === "error" ? "❌" : "Check Status"}
  </button>
      </div>
    </div>
  );
}
