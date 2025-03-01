from fastapi import FastAPI, File, UploadFile, Form
import shutil
from cloudinary_upload import upload_pdf  # Cloudinary function
from similarity_checker import check_pdf_similarity  # Similarity function

app = FastAPI()

# ✅ Upload API for Old Project Proposals (Now Includes Category)
@app.post("/upload/selectedproject/")
async def upload_file(file: UploadFile = File(...), category: str = Form(...)):
    file_path = f"./temp_{file.filename}"

    # ✅ Save the file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Call the Cloudinary upload function (Modify to store category in DB)
    upload_pdf(file_path ,category)

    return {"message": "File uploaded successfully!", "category": category}

# ✅ API for Checking Similarity of New Student Proposal (With Category)
@app.post("/check-similarity/")
async def check_similarity(file: UploadFile = File(...), category: str = Form(...)):
    return await check_pdf_similarity(file, category)

# ✅ Run the server using:
# uvicorn api:app --reload
