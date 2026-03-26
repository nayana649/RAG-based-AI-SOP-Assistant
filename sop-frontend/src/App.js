import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [showControls, setShowControls] = useState(false);
  const [isExit, setIsExit] = useState(false);

  const handleIndex = async () => {
    if (!file) return alert("Select a file first!");
    const formData = new FormData();
    formData.append("file", file);
    try {
      await axios.post("http://localhost:8000/upload", formData);
      alert("Document indexed! You can now ask multiple questions.");
      setStatusMessage("");
      setIsExit(false);
    } catch (err) { alert("Indexing failed."); }
  };

  const handleAsk = async () => {
    if (!query) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("query", query);
    try {
      const response = await axios.post("http://localhost:8000/chat", formData);
      const newEntry = {
        question: query,
        answer: response.data.answer,
        sources: response.data.sources
      };
      setChatHistory([newEntry, ...chatHistory]);
      setQuery("");
      // Logic for post-answer interaction
      setStatusMessage("THANK YOU USER!!!!");
      setShowControls(true);
    } catch (err) { alert("Error getting answer."); }
    setLoading(false);
  };

  const handleContinue = () => {
    setStatusMessage("PROCEED");
    setShowControls(false);
  };

  const handleExit = () => {
    setStatusMessage("VISIT AGAIN, HAVE A NICE DAY!!!");
    setShowControls(false);
    setIsExit(true); // Disable further input
  };

  return (
    <div className="App">
      <h1>DocuMind Enterprise</h1>
      
      {!isExit && (
        <div className="upload-box">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleIndex}>Index Document</button>
        </div>
      )}

      <h2 className="status-banner">{statusMessage}</h2>

      {!showControls && !isExit && (
        <div className="input-area">
          <input 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Ask anything about the document..."
          />
          <button onClick={handleAsk} disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      )}

      {showControls && (
        <div className="control-prompt">
          <p>Do you want to continue or exit?</p>
          <button className="btn-continue" onClick={handleContinue}>Continue</button>
          <button className="btn-exit" onClick={handleExit}>Exit</button>
        </div>
      )}

      <div className="chat-container">
        {chatHistory.map((item, index) => (
          <div key={index} className="chat-entry">
            <p><strong>You:</strong> {item.question}</p>
            <p><strong>DocuMind:</strong> {item.answer}</p>
            <small>Sources (Page): {item.sources.join(", ")}</small>
            <hr />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
