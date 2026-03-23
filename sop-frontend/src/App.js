import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF first!");
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      await fetch('http://localhost:8000/upload', { method: 'POST', body: formData });
      alert("SOP Document Uploaded and Indexed!");
    } catch (err) {
      alert("Upload failed.");
    }
    setLoading(false);
  };

  const handleChat = async () => {
    if (!query) return;
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await response.json();

      // Update chat with the answer AND the citations
      setChatHistory([...chatHistory, { 
        question: query, 
        answer: data.answer, 
        citations: data.citations 
      }]);
      setQuery('');
    } catch (err) {
      alert("Chat failed.");
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>DocuMind Enterprise AI</h1>
        <div className="upload-section">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleUpload} disabled={loading}>Upload SOP</button>
        </div>

        <div className="chat-window">
          {chatHistory.map((chat, i) => (
            <div key={i} className="message-pair">
              <p className="user-msg"><strong>You:</strong> {chat.question}</p>
              <div className="ai-msg">
                <p><strong>DocuMind:</strong> {chat.answer}</p>
                {chat.citations && chat.citations.length > 0 && (
                  <div className="citations">
                    <small>Verified Sources:</small>
                    <ul>
                      {chat.citations.map((c, j) => <li key={j}>{c}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="input-area">
          <input 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Ask a policy question..." 
          />
          <button onClick={handleChat} disabled={loading}>Ask</button>
        </div>
      </header>
    </div>
  );
}

export default App;