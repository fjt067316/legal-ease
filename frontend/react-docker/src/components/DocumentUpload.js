import React, { useState, useRef } from "react";
import "../App.css";
import * as pdfjs from 'pdfjs-dist';
import ResultDisplay from "./ResultDisplay";

// Set the worker source
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.mjs',
  import.meta.url
).toString();

function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState("");
  const [citations, setCitations] = useState([]);
  const [pdfText, setPdfText] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      extractTextFromPdf(selectedFile);
    } else {
      alert("Please select a PDF file");
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      setFileName(droppedFile.name);
      extractTextFromPdf(droppedFile);
    } else {
      alert("Please drop a PDF file");
    }
  };

  const extractTextFromPdf = async (pdfFile) => {
    try {
      // Read the file as ArrayBuffer
      const arrayBuffer = await pdfFile.arrayBuffer();
      
      // Load the PDF document
      const pdf = await pdfjs.getDocument({ data: arrayBuffer }).promise;
      
      let fullText = '';
      
      // Extract text from each page
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => item.str).join(' ');
        fullText += pageText + '\n';
      }
      
      setPdfText(fullText);
      console.log("Extracted text:", fullText);
    } catch (error) {
      console.error("Error extracting text from PDF:", error);
      alert("Failed to extract text from the PDF file.");
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    if (!pdfText) {
      alert("Failed to extract text from the PDF file");
      return;
    }

    setIsUploading(true);
    
    fetch("http://localhost:8000/api/analyzeLease", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        leaseText: pdfText 
      }),
    })
      .then(response => response.json())
      .then(data => {
        setIsUploading(false);
        setAnalysisResult(data.response || "Analysis completed. No response received.");
        setCitations(data.citations || []);
      })
      .catch(error => {
        console.error("Error analyzing lease:", error);
        setIsUploading(false);
        setAnalysisResult("An error occurred during analysis. Please try again.");
        setCitations([]);
      });
  };

  const handleReset = () => {
    setFile(null);
    setFileName("");
    setAnalysisResult("");
    setPdfText("");
    setCitations([]); // Reset citations
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="container">
      <div className="section pdf-upload-section">
        <h2>Upload Lease Agreement</h2>
        <p>Upload your lease agreement as a PDF to check for illegal clauses</p>
        
        {!analysisResult ? (
          <>
            <div 
              className={`drop-area ${isDragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={handleUploadClick}
            >
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileChange} 
                accept="application/pdf" 
                style={{ display: 'none' }}
              />
              {fileName ? (
                <div className="file-info">
                  <p>Selected file: {fileName}</p>
                  {pdfText && <p className="text-success">✓ Text extracted successfully</p>}
                </div>
              ) : (
                <div className="upload-prompt">
                  <p>Drag & drop your PDF here or click to browse</p>
                  <span className="upload-icon">📄</span>
                </div>
              )}
            </div>
            
            <div className="button-container">
              <button 
                onClick={handleSubmit} 
                className="button" 
                disabled={!file || !pdfText || isUploading}
              >
                {isUploading ? "Analyzing..." : "Submit for Analysis"}
              </button>
              {file && (
                <button onClick={handleReset} className="button secondary-button">
                  Reset
                </button>
              )}
            </div>
          </>
        ) : (
          <div className="analysis-result">
            {/* Use ResultDisplay component to show both result and citations */}
            <ResultDisplay 
              result={analysisResult} 
              query="Lease Analysis" 
              citations={citations} 
            />
            <button onClick={handleReset} className="button">
              Upload Another Document
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentUpload;