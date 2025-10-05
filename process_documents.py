"""
Document Processing Pipeline

This master script chains together all document processing steps:
1. Upload PDFs to Azure Blob Storage
2. Analyze documents with Azure Document Intelligence
3. Extract clean English text
4. Clean up temporary files

Usage: python3 process_documents.py
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def cleanup_temp_files():
    """Clean up temporary files to keep project tidy"""
    print(f"\n{'='*60}")
    print("CLEANUP: Removing temporary files")
    print(f"{'='*60}")
    
    temp_files = [
        "extract_english_text.py",  # This is a utility script, not needed after use
    ]
    
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️  Removed: {file}")
    
    # Clean up any other temporary files if needed
    print("✅ Cleanup complete")

def check_requirements():
    """Check if required files and environment are set up"""
    print(f"\n{'='*60}")
    print("CHECKING: Requirements and setup")
    print(f"{'='*60}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ ERROR: .env file not found!")
        print("Please copy env.example to .env and configure your Azure credentials")
        return False
    
    # Check if input_document folder exists and has PDFs
    if not os.path.exists('input_document'):
        print("❌ ERROR: input_document folder not found!")
        print("Please create the folder and add PDF files to process")
        return False
    
    pdf_files = [f for f in os.listdir('input_document') if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ ERROR: No PDF files found in input_document folder!")
        print("Please add PDF files to process")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF file(s): {', '.join(pdf_files)}")
    print("✅ .env file found")
    print("✅ All requirements met")
    return True

def create_output_summary():
    """Create a summary of all output files"""
    print(f"\n{'='*60}")
    print("OUTPUT SUMMARY")
    print(f"{'='*60}")
    
    output_files = []
    if os.path.exists('output'):
        for file in os.listdir('output'):
            file_path = os.path.join('output', file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                output_files.append((file, size))
    
    if output_files:
        print("Generated files:")
        for file, size in sorted(output_files):
            size_mb = size / (1024 * 1024)
            print(f"  📄 {file} ({size_mb:.2f} MB)")
    else:
        print("No output files found")

def main():
    """Main pipeline execution"""
    print("🚀 BHUTAN TRAINING DOCUMENT PROCESSING PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 0: Check requirements
    if not check_requirements():
        print("\n❌ PIPELINE FAILED: Requirements not met")
        sys.exit(1)
    
    # Step 1: Upload PDFs to blob storage
    if not run_script('upload_to_blob.py', 'Uploading PDFs to Azure Blob Storage'):
        print("\n❌ PIPELINE FAILED: Upload step failed")
        sys.exit(1)
    
    # Step 2: Analyze documents
    if not run_script('doc_intellegence.py', 'Analyzing documents with Azure Document Intelligence'):
        print("\n❌ PIPELINE FAILED: Document analysis failed")
        sys.exit(1)
    
    # Step 3: Extract English text
    if not run_script('extract_english_text.py', 'Extracting clean English text'):
        print("\n❌ PIPELINE FAILED: Text extraction failed")
        sys.exit(1)
    
    # Step 4: Cleanup
    cleanup_temp_files()
    
    # Step 5: Summary
    create_output_summary()
    
    print(f"\n{'='*60}")
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    print("\n📁 Check the 'output' folder for all generated files:")
    print("  • analysis_results.txt - Human-readable analysis")
    print("  • analysis_response.json - Complete JSON response")
    print("  • english_content.txt - Clean English text")

if __name__ == "__main__":
    main()
