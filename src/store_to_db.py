import fitz 
import psycopg2
import ollama







# ✅ Process PDF (Now Accepts PDF URL)
def process_pdf(pdf_path, pdf_url):
    pdf_name = pdf_path.split("/")[-1]
    text = extract_text_from_pdf(pdf_path)
    if text:
        vector = generate_embeddings(text)
        if vector:
            store_vectors_in_db(pdf_name, pdf_url, vector, text)  # ✅ Pass extracted_text
        else:
            print("❌ Failed to generate vector.")
    else:
        print("❌ Failed to extract text from PDF.")
