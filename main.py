import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from processor import process_pdf, get_answer 
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    process_pdf(file_path)
    return {"message": "Document indexed successfully"}

@app.post("/chat")
async def chat_endpoint(query: str = Form(...)):
    try:
        # Now calls get_answer with just the question
        result = get_answer(query)
        return result
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
