import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the processing function from your processor.py
from processor import process_pdf_with_citations, get_response

app = FastAPI(title="DocuMind Enterprise API")

# --- 1. Week 4: Security & Integration (CORS) ---
# This allows your React frontend (usually on port 3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the vector database in memory
# (In a larger app, you would use Pinecone as per your guide)
global_vector_store = None
current_file_path = None

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "DocuMind Enterprise API is running"}

# --- 2. Week 1: Ingestion Endpoint ---
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global global_vector_store, current_file_path
    
    # Save the uploaded file locally
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Process PDF and create FAISS index
        global_vector_store = process_pdf_with_citations(file_path)
        current_file_path = file_path
        return {"message": f"File {file.filename} processed successfully and indexed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. Week 2 & 3: Retrieval & Streaming Logic ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global global_vector_store
    
    if global_vector_store is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet. Please upload a document first.")
    
    try:
        # WEEK 4: Get response and the new Citations metadata
        # Note: We pass the file_path to processor for source naming
        result = get_response(request.query, global_vector_store, current_file_path)
        
        # Returns both the text answer and the specific page citations
        return {
            "answer": result["answer"],
            "citations": result["citations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)