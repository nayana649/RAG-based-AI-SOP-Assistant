import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Configuration & API Key
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

def process_pdf_with_citations(file_path):
    # WEEK 1: Ingestion Pipeline (Enhanced with Metadata)
    loader = PyPDFLoader(file_path)
    documents = loader.load() # This automatically captures 'page' metadata
    
    # Sophisticated Chunking (Week 1 Requirement)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)
    
    # Embedding & Vector Store (FAISS)
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)
    
    return vector_store

def get_response(query, vector_store):
    # WEEK 2 & 4: Safety Guardrails (Strict System Prompt)
    template = """
    You are the 'DocuMind Enterprise' Corporate Assistant. 
    Use ONLY the following pieces of context to answer the question. 
    
    GUARDRAILS:
    1. If the answer is not in the context, strictly say: "I don't know; this is outside my scope."
    2. Do NOT use any external knowledge. 
    3. Do NOT mention the context folders or technical details.

    CONTEXT:
    {context}

    QUESTION: 
    {question}

    ANSWER:
    """
    
    PROMPT = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )

    # Initialize LLM (Groq Llama 3)
    llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

    # WEEK 4: Retrieval with Metadata (Citations)
    # Search for top 3 relevant chunks
    docs = vector_store.similarity_search(query, k=3)
    
    # Extract Page Numbers and Source Names for Citations
    citations = []
    for d in docs:
        page_num = d.metadata.get('page', 0) + 1  # Index starts at 0, so add 1
        source = f"Source: {os.path.basename(file_path)} (Page {page_num})"
        if source not in citations:
            citations.append(source)

    # Create the Chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )

    result = chain.invoke({"query": query})
    
    # Return both the Answer and the Citations
    return {
        "answer": result["result"],
        "citations": citations
    }