import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import QueryInput from "./components/QueryInput";
import About from "./components/About";
import NavBar from "./components/NavBar";
import Header from "./components/Header";
import DocumentUpload from "./components/DocumentUpload";
import Footer from "./components/Footer"; // Import the Footer component

function App() {
  return (
    <div className="App">
      <NavBar />
      <div className="main-content">
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Header />
                <QueryInput />
              </>
            }
          />
          <Route path="/about" element={<About />} />
          <Route path="/document-upload" element={<DocumentUpload />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;