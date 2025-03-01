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


# ✅ Convert PostgreSQL vector string to NumPy array
def convert_string_to_vector(vector_str):
    try:
        vector_str = vector_str.strip("[]")  # Remove square brackets
        vector = np.array([float(x) for x in vector_str.split(",")])
        return vector
    except Exception as e:
        print("Error converting vector string:", e)
        return None


# ✅ Fetch stored vectors from PostgreSQL
def fetch_stored_vectors():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT pdf_url, embedding, extracted_text FROM pdf_vectors;")
        data = cur.fetchall()  # List of tuples (pdf_url, embedding, extracted_text)

        cur.close()
        conn.close()

        # Convert stored embeddings from string to NumPy arrays
        processed_data = [
            (pdf_url, convert_string_to_vector(embedding), extracted_text) for pdf_url, embedding, extracted_text in data
        ]

        return processed_data
    except Exception as e:
        print("❌ Error fetching stored vectors:", e)
        return []


# ✅ Calculate similarity scores and filter those above 10%
def calculate_similarity(new_vector, stored_vectors):
    results = []
    
    for pdf_url, stored_vector, extracted_text in stored_vectors:
        if stored_vector is not None:
            try:
                similarity = cosine_similarity([new_vector], [stored_vector])[0][0] * 100  # Convert to percentage
                similarity_percentage = round(similarity, 2)
                if similarity_percentage >= 10:  # Only consider PDFs with more than 10% similarity
                    results.append({
                        "pdf_url": pdf_url,
                        "similarity_score": similarity_percentage,
                        "extracted_text": extracted_text
                    })
            except Exception as e:
                print("Error calculating similarity:", e)

    return results


# ✅ API Function for Similarity Check
async def check_pdf_similarity(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file.file)
    if not pdf_text:
        return {"error": "Could not extract text from the PDF"}

    new_vector = generate_embeddings(pdf_text)
    if new_vector is None:
        return {"error": "Failed to generate embeddings"}

    stored_vectors = fetch_stored_vectors()
    if not stored_vectors:
        return {"error": "No stored projects found in the database"}

    matched_results = calculate_similarity(new_vector, stored_vectors)

    if not matched_results:
        return {"error": "No similar projects found."}

    # ✅ Compute overall average similarity score
    avg_score = sum(item["similarity_score"] for item in matched_results) / len(matched_results)

    # ✅ Generate LLM insights for each matched project
    final_results = []
    for match in matched_results:
        pdf_url = match["pdf_url"]
        similarity_score = match["similarity_score"]
        retrieved_text = match["extracted_text"]

        # Generate comparison summary using DeepSeek
        prompt = f"""
        You are an AI assistant for academic research. 
        Compare the following two documents:

        **New Document:** {pdf_text[:1000]}...

        **Stored Document:** {retrieved_text[:1000]}...

        Summarize the key differences and how similar they are.
        """

        response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt}])

        final_results.append({
            "pdf_url": pdf_url,
            "similarity_score": similarity_score,
            "llm_comparison_summary": response["message"]["content"]
        })

    return {
        "average_similarity_score": round(avg_score, 2),
        "matched_projects": final_results
    }
