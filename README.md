# DocuMind Enterprise: RAG-based SOP Analysis 🧠

Developed as part of my **Python Developer Internship** at **Infotact Solutions**, this project implements an advanced Retrieval-Augmented Generation (RAG) system for analyzing Standard Operating Procedures (SOPs).

## 🚀 Key Features
- **Intelligent Retrieval:** Uses LangChain and Llama-3.1-8b-instant to provide accurate answers.
- **Automated Citations:** Extracts and verifies page numbers from source PDFs.
- **Privacy & Cost-Efficient:** Leverages local HuggingFace embeddings (`all-MiniLM-L6-v2`) to eliminate API costs.
- **DevOps Ready:** Fully containerized with a `Dockerfile` and secured via `.env` management.

## 🛠️ Technical Stack
- **Backend:** FastAPI, Python 3.10
- **AI Framework:** LangChain-Classic 2026
- **Vector Store:** FAISS
- **Frontend:** React.js

## 📦 Setup Instructions
1. **Clone the repository.**
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure Environment:** Add your `GROQ_API_KEY` to the `.env` file.
4. **Run Backend:** `python main.py`
5. **Run Frontend:** `cd sop-frontend && npm start`

   ## 🚀 How to Run DocuMind Enterprise

To get the application running locally for your **Infotact Solutions** review, follow these steps:

### **Terminal 1: Backend (FastAPI)**
1. Open a terminal in the root folder (`my_rag_project`).
2. Activate the environment: `.\sop_env\Scripts\activate`
3. Start the server: `python main.py`

### **Terminal 2: Frontend (React)**
1. Open a **second** terminal window.
2. Navigate to the frontend: `cd sop-frontend`
3. Launch the UI: `npm start`
