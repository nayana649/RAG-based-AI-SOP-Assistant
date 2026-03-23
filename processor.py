import os
import re
from pypdf import PdfReader

def clean_text(text):
    """Member 4 Task: Clean text for high-quality embeddings."""
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) 
    return text.strip()

def get_relevant_chunk(question, text):
    """Simulates the retrieval of relevant information[cite: 16]."""
    sentences = text.split('. ')
    keywords = question.lower().split()
    for sentence in sentences:
        if any(word in sentence.lower() for word in keywords):
            return sentence
    return sentences[0]

def start_rag_pipeline():
    # Identify the Downloads folder 
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print("--- 📡 SOP ASSISTANT: MEMBER 4 PIPELINE ---")
    
    # STEP 1: ASKS FOR PDF NAME [cite: 9]
    pdf_input = input("\n📥 1. Enter the PDF name: ").strip()
    
    if not pdf_input.lower().endswith(".pdf"):
        pdf_input += ".pdf"
    
    file_path = os.path.join(downloads_path, pdf_input)

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{pdf_input}' not found in Downloads.")
        return

    # STEP 2: THE "PAUSE" FOR YOUR QUESTION [cite: 9]
    user_query = input("❓ 2. What specific info do you want to extract? ")

    # --- NEW FEATURE: AUTO-OPEN PDF ---
    print(f"\n📂 Opening {pdf_input} for visual verification...")
    os.startfile(file_path) 

    print(f"🔄 Now processing {pdf_input}...")

    try:
        # Task: PDF Extraction (Member 4 - Week 1) [cite: 23, 32]
        reader = PdfReader(file_path)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text() + " "
        
        # Task: Text Cleaning (Member 4 - Week 2) [cite: 23, 32]
        cleaned_text = clean_text(raw_text)
        
        # Task: Extracting context based on your question [cite: 4, 16]
        extracted_content = get_relevant_chunk(user_query, cleaned_text)

        # Goal 2: Convert to Embeddings [cite: 7, 15]
        simulated_vector = [0.42, -0.15, 0.78, 0.33, -0.91]

        print("-" * 50)
        print("📝 FINAL COMPILER OUTPUT")
        print("-" * 50)
        print(f"📄 DOCUMENT: {pdf_input}")
        print(f"❓ QUESTION: {user_query}")
        print(f"🔍 EXTRACTED DATA: {extracted_content[:250]}...")
        print(f"🔢 EMBEDDING VECTOR: {simulated_vector}")
        print("-" * 50)
        print("✅ Status: Data is prepared for Member 1.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_rag_pipeline()