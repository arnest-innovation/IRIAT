from fastapi import FastAPI, File, UploadFile
import shutil
from cloudinary_upload import upload_pdf  # Cloudinary function
from similarity_checker import check_pdf_similarity  # Similarity function

app = FastAPI()

# ✅ Upload API for Old Project Proposals
@app.post("/upload/selectedproject/")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"./temp_{file.filename}"

    # ✅ Save the file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Call the Cloudinary upload function
    upload_pdf(file_path)

    return {"message": "File uploaded successfully!"}

# ✅ API for Checking Similarity of New Student Proposal
@app.post("/check-similarity/")
async def check_similarity(file: UploadFile = File(...)):
    return await check_pdf_similarity(file)

# ✅ Run the server using:
# uvicorn api:app --reload
