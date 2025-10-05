"""
Azure Blob Storage Upload Script

This script uploads all PDF files from the input_document folder to Azure Blob Storage.
It uses environment variables for secure credential management.

Features:
- Uploads all PDF files from ./input_document folder
- Uses Azure Blob Storage with SAS token authentication
- Environment variable configuration for security
- Overwrites existing files with same name

Requirements:
- AZURE_CONTAINER_URL environment variable in .env file
- PDF files in ./input_document folder
- Required packages in requirements.txt

Usage: python3 upload_to_blob.py
"""

import os
from azure.storage.blob import BlobClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
input_folder = "./input_document"

# Get container URL from environment variables
container_url = os.getenv("AZURE_CONTAINER_URL")
if not container_url:
    raise ValueError("AZURE_CONTAINER_URL environment variable is not set. Please check your .env file.")

def upload_files():
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(input_folder, filename)
        
        # Correct: append filename BEFORE the SAS token
        blob_url = f"https://datubox.blob.core.windows.net/bhutan-box/{filename}?{container_url.split('?')[1]}"

        blob = BlobClient.from_blob_url(blob_url)

        with open(file_path, "rb") as data:
            blob.upload_blob(data, overwrite=True)
            print(f"Uploaded: {filename}")

if __name__ == "__main__":
    upload_files()
