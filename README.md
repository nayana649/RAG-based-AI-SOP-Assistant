# AI-SOP-Assistant (RAG Architecture)

A full-stack AI application designed to help teams query Standard Operating Procedures (SOPs) using Retrieval-Augmented Generation.

## 🏗️ System Architecture
The project follows a modular RAG flow:
1. **Frontend**: React-based UI for document upload and chat interface.
2. **Backend**: FastAPI server handling API requests.
3. **AI Engine**: PDF text extraction and FAISS Vector Storage.
4. **LLM**: Groq (Llama 3) for context-aware response generation.

## 🛠️ Technical Implementation

I built this entire RAG (Retrieval-Augmented Generation) pipeline from scratch, handling the full development lifecycle:

* **Frontend**: Developed a responsive chat and upload interface using **React.js**.
* **Backend**: Built a high-performance API with **Python** and **FastAPI**.
* **AI Engine**: Implemented document intelligence using **PyPDF2** for extraction.
* **LLM Integration**: Connected the system to **Groq (Llama 3)** for ultra-fast, context-aware responses.
* **DevOps**: Managed version control via **Git/GitHub** and optimized the environment with custom `.gitignore` configurations.

## 🚀 Key Features
- **Context-Aware Q&A**: Answers are strictly based on the uploaded SOP content.
- **Fast Inference**: Leveraged Groq's API for near-instant response times.
- **Dynamic Indexing**: Documents are processed and indexed in real-time upon upload.
