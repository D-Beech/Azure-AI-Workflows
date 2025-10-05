# Bhutan Training Document Analysis

A complete document processing pipeline using Azure services for analyzing PDF documents, uploading to blob storage, and extracting English text content.

## Features

- **Document Analysis**: Uses Azure Document Intelligence to extract text, tables, and structure from PDFs
- **Blob Storage Upload**: Uploads PDF files to Azure Blob Storage with SAS token authentication
- **English Text Extraction**: Filters and extracts clean English text from document analysis results
- **Environment-based Configuration**: Secure credential management using environment variables

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp env.example .env
```

3. **Edit `.env` with your Azure credentials:**
```bash
# Azure Blob Storage Configuration
AZURE_CONTAINER_URL=https://your-storage-account.blob.core.windows.net/container-name?sp=racwd&st=...

# Azure Document Intelligence Configuration  
AZURE_FORM_RECOGNIZER_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=your-api-key-here

# Sample Document URL (optional)
SAMPLE_DOCUMENT_URL=https://raw.githubusercontent.com/Azure-Samples/...
```

## Usage

### Quick Start (Recommended)
```bash
python3 process_documents.py
```
**One-command pipeline** that runs all steps automatically:
1. Checks requirements and setup
2. Uploads PDFs to Azure Blob Storage
3. Analyzes documents with Azure Document Intelligence
4. Extracts clean English text
5. Creates LLM-ready text chunks
6. Cleans up temporary files
7. Shows output summary

### Individual Scripts

#### 1. Upload PDFs to Blob Storage
```bash
python3 upload_to_blob.py
```
- Uploads all PDF files from `./input_document` folder
- Uses SAS token authentication from environment variables

#### 2. Analyze Documents
```bash
python3 doc_intellegence.py
```
- Analyzes documents using Azure Document Intelligence
- Saves results to:
  - `./output/analysis_results.txt` (human-readable format)
  - `./output/analysis_response.json` (complete JSON response)

#### 3. Extract English Text
```bash
python3 extract_english_text.py
```
- Extracts clean English text from analysis results
- Saves to `./output/english_content.txt`

#### 4. Create LLM Chunks
```bash
python3 chunk_for_llm.py
```
- Creates text chunks optimized for LLM ingestion
- Configurable token size (default: 500) and overlap (default: 50)
- Saves to `./output/llm_chunks.json`

## Output Files

- `analysis_results.txt` - Human-readable document analysis
- `analysis_response.json` - Complete Azure API response
- `english_content.txt` - Clean English text only
- `llm_chunks.json` - LLM-ready text chunks with configurable size/overlap

## Project Structure

```
bhutan_training/
├── input_document/          # PDF files to process
├── output/                  # Generated analysis files
├── process_documents.py     # 🚀 Master pipeline script (recommended)
├── doc_intellegence.py      # Document analysis script
├── upload_to_blob.py        # Blob storage upload script
├── extract_english_text.py  # English text extraction
├── chunk_for_llm.py         # LLM text chunking
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create from env.example)
└── README.md               # This file
```

## Requirements

- Python 3.8 or later
- Azure Document Intelligence resource
- Azure Blob Storage account
- Required packages listed in `requirements.txt`

## Environment Variables

- `AZURE_CONTAINER_URL`: Blob storage container URL with SAS token
- `AZURE_FORM_RECOGNIZER_ENDPOINT`: Document Intelligence endpoint
- `AZURE_FORM_RECOGNIZER_KEY`: Document Intelligence API key
- `SAMPLE_DOCUMENT_URL`: Optional sample document URL
