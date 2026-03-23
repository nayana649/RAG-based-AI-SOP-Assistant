import os
import re
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DeterministicFakeEmbedding
from groq import Groq

app = FastAPI()

# Member 5: Update this with your Vercel URL later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq (Set your API Key in your terminal/environment)
# For now, you can paste your key directly: client = Groq(api_key="your_key_here")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

vector_db = None

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global vector_db
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    try:
        pdf_reader = PdfReader(file.file)
        raw_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        cleaned_text = clean_text(raw_text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = text_splitter.split_text(cleaned_text)
        embeddings = DeterministicFakeEmbedding(size=1536)
        vector_db = FAISS.from_texts(chunks, embeddings)
        return {"message": "SOP Indexed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(data: dict):
    global vector_db
    if not vector_db:
        raise HTTPException(status_code=400, detail="Please upload a document first.")
    
    query = data.get("question")
    docs = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # AI Generation Step
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are a helpful SOP Assistant. Answer based ONLY on this context: {context}"},
            {"role": "user", "content": query}
        ],
        model= "llama-3.3-70b-versatile",
    )
    return {"answer": response.choices[0].message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)