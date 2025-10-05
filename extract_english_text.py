import json
import re

def is_english(text):
    """Check if text is primarily English"""
    if not text:
        return False
    english_chars = len(re.findall(r'[a-zA-Z\s]', text))
    total_chars = len(text.strip())
    if total_chars == 0:
        return False
    return english_chars / total_chars > 0.7

def extract_english_text(json_file_path):
    """Extract all English text from the document"""
    
    # Load the JSON response
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the main content string
    main_content = data.get('content', '')
    
    # Split into lines and filter for English
    lines = main_content.split('\n')
    english_lines = []
    
    for line in lines:
        line = line.strip()
        if line and is_english(line):
            english_lines.append(line)
    
    # Join all English lines
    english_text = '\n'.join(english_lines)
    
    # Save to text file
    output_file = "./output/english_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(english_text)
    
    print(f"Extracted English content to {output_file}")
    print(f"Total lines: {len(english_lines)}")
    print(f"Total characters: {len(english_text)}")
    
    return english_text

if __name__ == "__main__":
    extract_english_text("./output/analysis_response.json")
