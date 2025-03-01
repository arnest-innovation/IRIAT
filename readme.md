# **PDF Similarity Checker using AI (DeepSeek + PostgreSQL + pgVector)**

## **Project Overview**
This project is designed to **compare the similarity of PDF documents** by converting them into **vector embeddings** using **DeepSeek-R1 (via Ollama)** and storing these embeddings in **PostgreSQL with pgVector extension**. The system helps in verifying **originality and uniqueness** of academic or research documents by computing similarity scores.

---

## **Requirements**
Before setting up the project, ensure you have installed the following dependencies:

- **PostgreSQL** (Database for storing embeddings)
- **pgVector extension** (Vector storage & similarity search in PostgreSQL)
- **pgAdmin4** (Optional: GUI for PostgreSQL management)
- **Ollama** (Runs the DeepSeek model locally for embedding generation)
- **DeepSeek-R1 model** (1.5B parameter model for embeddings)
- **Python 3.x**
- **VS Code** (or any Python IDE for development)

---

## **Setup Instructions**

### **1️⃣ Setting up Ollama**
Ollama is used to generate vector embeddings for PDF text.

1. **Start Ollama in the background**
   ```sh
   ollama serve
   ```

2. **Check if Ollama is running**
   ```sh
   pgrep ollama
   ```
   (If it returns a process ID, Ollama is running successfully.)

3. **Stop Ollama if needed**
   ```sh
   pkill ollama  # Kill the running process
   ```
   OR
   ```sh
   kill -9 $(pgrep ollama)  # Force kill
   ```

---

### **2️⃣ Setting up PostgreSQL**
PostgreSQL is used for **storing extracted text embeddings** and performing **vector similarity searches**.

1. **Start PostgreSQL**
   ```sh
   brew services start postgresql@17
   ```

2. **Check PostgreSQL service status**
   ```sh
   brew services list
   ```

3. **Stop PostgreSQL if needed**
   ```sh
   brew services stop postgresql@17
   ```

4. **Access PostgreSQL shell**
   ```sh
   psql -U your_username -d postgres
   ```
   (Replace `your_username` with your actual PostgreSQL user.)

5. **Exit PostgreSQL shell**
   ```sh
   \q
   ```

---

### **3️⃣ Clone the Project & Install Dependencies**

1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/pdf-similarity-checker.git
   cd pdf-similarity-checker
   ```

2. **Create a Python Virtual Environment**
   ```sh
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```sh
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

4. **Install dependencies from `requirements.txt`**
   ```sh
   pip install -r requirements.txt
   ```

---

### **4️⃣ Run the API Server**
1. **Navigate to the `src` directory**
   ```sh
   cd src
   ```
2. **Run the FastAPI server**
   ```sh
   uvicorn api:app --reload
   ```
3. **Test the API in your browser**
   - Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI for API testing) OR Postman

---

## **Modules & Their Usage**
### **🔹 PyMuPDF (fitz)**
- Used for **extracting text** from PDFs. It supports complex PDF structures and ensures reliable text extraction.

### **🔹 Ollama**
- Runs the **DeepSeek-R1:1.5B** model to generate **vector embeddings** for the extracted text.

### **🔹 PostgreSQL + pgVector**
- Stores **vector embeddings** and allows **similarity search** using **cosine similarity**.

### **🔹 scikit-learn (cosine similarity)**
- Computes similarity scores between document embeddings.

### **🔹 FastAPI**
- Provides an **API endpoint** for uploading PDFs and checking similarity with stored PDFs.

---

## **📌 Project Functionality**
This project helps **compare PDF documents** for **similarity detection** using **AI-generated embeddings**. The primary goal is to assist **educators, researchers, and organizations** in verifying **document originality** efficiently.

- Upload a **new PDF**
- Convert it into **vector embeddings** using **DeepSeek-R1**
- Compare it with **stored PDFs in the database**
- Return a **similarity score (0-100%)**
- Use **LLM-based insights** to describe document differences

---

✅ Now your **PDF Similarity Checker** is set up and ready to use! 🚀

