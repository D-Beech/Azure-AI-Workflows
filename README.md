# Azure Blob Upload Script

Minimal script to upload files from `input_document` folder to Azure Blob Storage.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. **Copy the example environment file:**
```bash
cp env.example .env
```

2. **Edit `.env` with your values:**
```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=datubox;AccountKey=YOUR_ACCOUNT_KEY;EndpointSuffix=core.windows.net
CONTAINER_NAME=bhutan-box
INPUT_FOLDER=input_document
```

3. **Run the script:**
```bash
python upload_to_blob.py
```

## Environment Variables:
- `AZURE_STORAGE_CONNECTION_STRING`: Your Azure Storage connection string
- `CONTAINER_NAME`: Blob container name
- `INPUT_FOLDER`: Local folder to upload (optional, defaults to 'input_document')
