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
