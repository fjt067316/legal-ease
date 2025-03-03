import React from "react";
import { Routes, Route } from "react-router-dom"; // No extra BrowserRouter
import "./App.css";
import QueryInput from "./components/QueryInput";
import About from "./components/About"; // Ensure About component is imported
import NavBar from "./components/NavBar";
import Header from "./components/Header";
import DocumentUpload from "./components/DocumentUpload";

function App() {
  return (
    <div className="App">
      
      <NavBar />
      {/* <Header /> */}
      <Routes>
        <Route path="/" element={
           <>
           <Header />  
           <QueryInput />  
         </>
          } />
        <Route path="/about" element={<About />} />
        <Route path="/document-upload" element={<DocumentUpload />} />
      </Routes>
    </div>
  );
}

export default App;
