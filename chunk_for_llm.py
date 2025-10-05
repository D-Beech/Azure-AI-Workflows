"""
LLM Text Chunker

Creates text chunks optimized for LLM ingestion with configurable token size and overlap.
Uses simple word-based token estimation (1 token ≈ 4 characters).

Usage: python3 chunk_for_llm.py
"""

import json
import os

# Configuration - Easy to adjust
CHUNK_SIZE_TOKENS = 500
OVERLAP_TOKENS = 50
INPUT_FILE = "./output/english_content.txt"
OUTPUT_FILE = "./output/llm_chunks.json"

def estimate_tokens(text):
    """Simple token estimation: 1 token ≈ 4 characters"""
    return len(text) // 4

def chunk_text(text, chunk_size, overlap):
    """Split text into chunks with overlap"""
    chunks = []
    chunk_id = 1
    
    # Calculate chunk size in characters
    chunk_chars = chunk_size * 4  # 4 chars per token
    overlap_chars = overlap * 4
    
    start = 0
    while start < len(text):
        # Get chunk end position
        end = min(start + chunk_chars, len(text))
        
        # Try to break at word boundary
        if end < len(text):
            # Look for last space within reasonable distance
            search_start = max(start + chunk_chars - 50, start)
            last_space = text.rfind(' ', search_start, end)
            if last_space > search_start:
                end = last_space
        
        # Extract chunk
        chunk_text = text[start:end].strip()
        
        # Skip if chunk is too small
        if len(chunk_text) < 50:
            break
            
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })
        
        chunk_id += 1
        
        # Move start position with overlap
        start = end - overlap_chars
        
        # Prevent infinite loop
        if start >= len(text) - overlap_chars:
            break
    
    return chunks

def main():
    """Main chunking function"""
    print(f"🔪 Chunking text for LLM ingestion")
    print(f"Chunk size: {CHUNK_SIZE_TOKENS} tokens")
    print(f"Overlap: {OVERLAP_TOKENS} tokens")
    print(f"Input: {INPUT_FILE}")
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found!")
        print("Run the document processing pipeline first.")
        return
    
    # Read input text
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        print(f"❌ Error: {INPUT_FILE} is empty!")
        return
    
    print(f"📄 Input text: {len(text)} characters")
    print(f"📊 Estimated tokens: {estimate_tokens(text)}")
    
    # Create chunks
    chunks = chunk_text(text, CHUNK_SIZE_TOKENS, OVERLAP_TOKENS)
    
    if not chunks:
        print("❌ Error: No chunks created!")
        return
    
    # Save chunks
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    # Statistics
    total_chars = sum(len(chunk['text']) for chunk in chunks)
    avg_tokens = sum(estimate_tokens(chunk['text']) for chunk in chunks) // len(chunks)
    
    print(f"✅ Created {len(chunks)} chunks")
    print(f"📊 Average tokens per chunk: {avg_tokens}")
    print(f"📄 Total characters: {total_chars}")
    print(f"💾 Saved to: {OUTPUT_FILE}")
    
    # Show first chunk as example
    if chunks:
        print(f"\n📝 First chunk preview:")
        print(f"Chunk {chunks[0]['chunk_id']}: {chunks[0]['text'][:100]}...")

if __name__ == "__main__":
    main()
