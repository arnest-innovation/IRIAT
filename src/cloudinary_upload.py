import cloudinary
import cloudinary.uploader
import cloudinary.api
from store_to_db import process_pdf  # Import function from your db file

# ✅ Cloudinary Configuration
cloudinary.config(
    cloud_name="dg3djk3zp",
    api_key="336482269747555",
    api_secret="SrgDYxOJwOUcXctL16vaZzhW4sw",
    secure=True
)

# ✅ Function to Upload PDF & Call DB Storage
def upload_pdf(file_path ,category):
    response = cloudinary.uploader.upload(
        file_path, 
        resource_type="raw",  # Important for PDFs
        access_mode="public"  # Ensures public access
    )
    pdf_url = response["secure_url"]
    print("Uploaded PDF URL:", pdf_url)

    # ✅ Call the function from `store_to_db.py`
    process_pdf(file_path, pdf_url , category)

# ✅ Example Usage
if __name__ == "__main__":
    file_path = "/Users/gauravpatil/Documents/proposal2.pdf"  
    upload_pdf(file_path)
