"""
Training Data Generator

Generates Q&A pairs from document chunks for finetuning.
Usage: python3 openai_chat.py
"""

import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def generate_qa(client, chunk_text, chunk_id):
    """Generate 3 Q&A pairs for a chunk"""
    prompt = f"""Generate 3 Q&A pairs from this legal document:


{chunk_text}

Focus on: concepts, procedures, details, relationships.
Return JSON ONLY in this format:
[{{"question": "...", "answer": "..."}}]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate Q&A pairs for legal document training. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        print("Raw model output:", content)

        # If model wrapped response in code fences, strip them
        if content.startswith("```"):
            content = content.strip("`").split("json")[-1].strip()

        return json.loads(content)

    except Exception as e:
        print(f"⚠️ Failed to parse JSON for chunk {chunk_id}: {e}")
        return []


def main():
    client = OpenAI()
    
    # Load chunks
    with open("./output/llm_chunks.json", 'r') as f:
        chunks = json.load(f)
    
    training_data = []
    
    # Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)}...")
        
        qa_pairs = generate_qa(client, chunk['text'], chunk['chunk_id'])
        
        # Add metadata
        for qa in qa_pairs:
            qa.update({
                'chunk_id': chunk['chunk_id'],
            })
            training_data.append(qa)
        
        print(f"  → {len(qa_pairs)} Q&A pairs")
    
    # Save results
    with open("./output/training_data.json", 'w') as f:
        json.dump(training_data, f, indent=2)
    
    print(f"\n✅ {len(training_data)} total Q&A pairs saved")

if __name__ == "__main__":
    main()
