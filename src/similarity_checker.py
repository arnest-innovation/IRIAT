import psycopg2
import ollama
import fitz  # PyMuPDF for PDF text extraction
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import File, UploadFile
from store_to_db import DB_CONFIG  # Importing DB config


# ✅ Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file):
    text = ""
    try:
        if isinstance(file, str):  # If it's a file path
            pdf_document = fitz.open(file)
        else:  # If it's an uploaded file (binary)
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")

        print(f"Total Pages in PDF: {len(pdf_document)}")  # ✅ Check Total Pages

        for page_num, page in enumerate(pdf_document):
            extracted_text = page.get_text("text")
            if extracted_text:
                text += extracted_text + " "
                print(f"Page {page_num + 1} Text Length: {len(extracted_text)}")

        normalized_text = " ".join(text.split())  # Normalize text
        print("Extracted Full Text Length:", len(normalized_text))
        return normalized_text
    except Exception as e:
        print("❌ Error extracting text from PDF:", e)
        return None


# ✅ Generate embedding for the new PDF
def generate_embeddings(text):
    try:
        print("Generating embeddings for text:", text[:500])
        response = ollama.embeddings(model="deepseek-r1:1.5b", prompt=text)
        embedding = np.array(response["embedding"])
        return embedding
    except Exception as e:
        print("❌ Error generating embeddings:", e)
        return None


