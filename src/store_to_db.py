import fitz 
import psycopg2
import ollama


# ✅ Database Connection
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "gaurav@2350",
    "host": "localhost",
    "port": "5432"
}


# ✅ Extract text from PDF using PyMuPDF with debugging
def extract_text_from_pdf(file):
    text = ""
    try:
        # Handle both file upload (binary) and stored PDFs (path)
        if isinstance(file, str):  # If it's a file path
            pdf_document = fitz.open(file)
        else:  # If it's an uploaded file (binary)
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")

        print(f"Total Pages in PDF: {len(pdf_document)}")  # ✅ Check Total Pages

        for page_num, page in enumerate(pdf_document):
            extracted_text = page.get_text("text")  # Extract visible text
            if extracted_text:
                text += extracted_text + " "  # Add space between pages
                print(f"Page {page_num + 1} Text Length: {len(extracted_text)}")  # ✅ Check text length per page

        normalized_text = " ".join(text.split())  # Normalize text
        print("Extracted Full Text Length:", len(normalized_text))  # ✅ Check Total Extracted Text Length
        print("Extracted Full Text Preview:", normalized_text[:1000])  # ✅ Preview First 1000 Chars
        return normalized_text
    except Exception as e:
        print("❌ Error extracting text from PDF:", e)
        return None



# ✅ Generate Vector Embeddings
def generate_embeddings(text):
    try:
        print("Generating embeddings for text:", text[:500])  # Print first 500 characters
        response = ollama.embeddings(model="deepseek-r1:7b", prompt=text)
        embedding = response["embedding"]
        return embedding
    except Exception as e:
        print("❌ Error generating embeddings:", e)
        return None



# ✅ Store PDF Data in PostgreSQL (Updated to include category)
def store_vectors_in_db(pdf_name, pdf_url, vector, extracted_text, category):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # ✅ Create table with category column
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pdf_vectors (
                id SERIAL PRIMARY KEY,
                pdf_name TEXT,
                pdf_url TEXT,
                extracted_text TEXT,
                embedding vector(3584),
                category TEXT  -- ✅ New field for project category
            );
        """)

        vector_str = "[" + ",".join(map(str, vector)) + "]"

        # ✅ Insert data including the category
        cur.execute("INSERT INTO pdf_vectors (pdf_name, pdf_url, embedding, extracted_text, category) VALUES (%s, %s, %s::vector, %s, %s)",
                    (pdf_name, pdf_url, vector_str, extracted_text, category))

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ PDF uploaded successfully with extracted text and category '{category}'!")
    except Exception as e:
        print("❌ Error:", e)



# ✅ Process PDF (Now Accepts Category)
def process_pdf(pdf_path, pdf_url, category):
    pdf_name = pdf_path.split("/")[-1]
    text = extract_text_from_pdf(pdf_path)
    if text:
        vector = generate_embeddings(text)
        if vector:
            store_vectors_in_db(pdf_name, pdf_url, vector, text, category)  # ✅ Pass category
        else:
            print("❌ Failed to generate vector.")
    else:
        print("❌ Failed to extract text from PDF.")
