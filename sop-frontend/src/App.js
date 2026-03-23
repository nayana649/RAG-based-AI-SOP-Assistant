import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);
  const [status, setStatus] = useState("Idle");

  const handleUpload = async () => {
    if (!file) return alert("Select a file first!");
    const formData = new FormData();
    formData.append("file", file);
    setStatus("Indexing...");
    try {
      await axios.post("http://localhost:8000/upload", formData);
      setStatus("Document Ready!");
    } catch (err) { setStatus("Upload Error."); }
  };

  const handleAsk = async () => {
    if (!question) return;
    const newChat = [...chat, { role: "user", text: question }];
    setChat(newChat);
    setStatus("AI is thinking...");
    try {
      const response = await axios.post("http://localhost:8000/ask", { question });
      setChat([...newChat, { role: "ai", text: response.data.answer }]);
      setQuestion("");
      setStatus("Document Ready!");
    } catch (err) { setStatus("Error getting answer."); }
  };

  // Styles
  const btnStyle = { padding: '10px 20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' };
  const bubble = (role) => ({
    padding: '10px', margin: '5px', borderRadius: '10px', 
    backgroundColor: role === 'user' ? '#e1ffc7' : '#f1f0f0',
    alignSelf: role === 'user' ? 'flex-end' : 'flex-start',
    maxWidth: '70%'
  });

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', display: 'flex', flexDirection: 'column', height: '90vh' }}>
      <h2>📄 AI SOP Assistant</h2>
      <div>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} style={btnStyle}>Upload</button>
        <span style={{ marginLeft: '10px' }}>Status: <b>{status}</b></span>
      </div>

      <div style={{ flex: 1, border: '1px solid #ccc', margin: '20px 0', padding: '10px', overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
        {chat.map((msg, i) => <div key={i} style={bubble(msg.role)}><b>{msg.role}:</b> {msg.text}</div>)}
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <input style={{ flex: 1, padding: '10px' }} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask about the document..." />
        <button onClick={handleAsk} style={btnStyle}>Send</button>
        <button onClick={() => setChat([])} style={{...btnStyle, backgroundColor: '#dc3545'}}>Clear</button>
      </div>
    </div>
  );
}
export default App;