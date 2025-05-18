#!/usr/bin/env python3
import sys
import re
import os
import glob

def convert_vtt_to_text(input_file, output_folder):
    """Convert a WebVTT file to plain text, removing timestamps and formatting tags."""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines
    lines = content.split('\n')
    
    # Skip header (usually first line is "WEBVTT" and the following lines are metadata)
    start_index = 0
    for i, line in enumerate(lines):
        if line == "WEBVTT":
            start_index = i + 1
            break
    
    # Skip metadata lines
    while start_index < len(lines) and (lines[start_index].startswith("Kind:") or 
                                      lines[start_index].startswith("Language:") or 
                                      not lines[start_index].strip()):
        start_index += 1
    
    # Extract text content
    transcript = []
    last_line = ""  # To track unique text lines
    
    # Process each line
    i = start_index
    while i < len(lines):
        line = lines[i]
        
        # Skip timestamp lines and alignment lines
        if "-->" in line or "align:" in line or "position:" in line or not line.strip():
            i += 1
            continue
        
        # Remove formatting tags like <00:00:00.480> and <c> tags
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        
        # Skip empty lines or lines with just non-alphabetic characters
        if not clean_line or (len(clean_line) == 1 and not clean_line.isalpha()):
            i += 1
            continue
        
        # Add to transcript if it's a new line (not seen before)
        if clean_line and clean_line != last_line:
            transcript.append(clean_line)
            last_line = clean_line
        
        i += 1
    
    # Join the transcript lines
    output_text = "\n".join(transcript)
    
    # Output filename based on input filename
    base_name = os.path.basename(os.path.splitext(input_file)[0])
    output_file = os.path.join(output_folder, f"{base_name}.txt")
    
    # Write the output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    return output_file

def process_folder(input_folder):
    """Process all VTT files in a folder and convert them to text files."""
    # Create output folder name
    parent_folder = os.path.dirname(input_folder.rstrip('/'))
    folder_name = os.path.basename(input_folder.rstrip('/'))
    output_folder = os.path.join(parent_folder, f"output_{folder_name}")
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find all VTT files in the input folder
    vtt_files = glob.glob(os.path.join(input_folder, "*.vtt"))
    if not vtt_files:
        print(f"No VTT files found in {input_folder}")
        return
    
    # Process each VTT file
    processed_files = 0
    for vtt_file in vtt_files:
        try:
            output_file = convert_vtt_to_text(vtt_file, output_folder)
            print(f"Converted: {vtt_file} -> {output_file}")
            processed_files += 1
        except Exception as e:
            print(f"Error processing {vtt_file}: {str(e)}")
    
    print(f"Conversion complete! Processed {processed_files} files. Output saved to: {output_folder}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vtt_to_text.py <input_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' not found.")
        sys.exit(1)
    
    if not os.path.isdir(input_folder):
        print(f"Error: '{input_folder}' is not a directory.")
        sys.exit(1)
    
    process_folder(input_folder) 