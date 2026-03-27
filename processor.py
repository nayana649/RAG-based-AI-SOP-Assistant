import os
import warnings
import logging

# 1. Block the 'embeddings.position_ids' warning specifically
warnings.filterwarnings("ignore", message=".*embeddings.position_ids.*")

# 2. Force the transformers library (HuggingFace) to be quiet
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    
    # Save the index for multi-question support
    vector_db = FAISS.from_documents(splits, embeddings)
    vector_db.save_local("faiss_index")
    print("SUCCESS: FAISS Index created and saved.")
    return True

def get_answer(query):
    if not os.path.exists("faiss_index"):
        return {"answer": "Error: Please index the document first.", "sources": []}

    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever()
    
    # Updated Llama 3.1 model - temperature 0 ensures it follows instructions strictly
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    
    # MODIFIED TEMPLATE: Strict Instruction for Irrelevant Questions
    template = """You are a professional corporate assistant.
    Use ONLY the provided context to answer the question.
    
    RULE: If the information is not contained in the context below, 
    strictly respond with: "I Don't know".
    
    Do not use any outside knowledge or provide general information.

    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    answer = chain.invoke(query)
    
    # If the answer is the refusal phrase, return no sources
    if "I Don't know" in answer:
        return {"answer": "I Don't know", "sources": []}
    
    docs = retriever.invoke(query)
    sources = list(set([str(doc.metadata.get("page", "N/A")) for doc in docs]))
    
    return {"answer": answer, "sources": sources}
