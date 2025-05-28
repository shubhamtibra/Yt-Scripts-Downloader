#!/usr/bin/env python3
import os
import math
import argparse

def split_file(input_file, num_parts=10):
    """Split a text file into equal parts."""
    # Get file size
    file_size = os.path.getsize(input_file)
    
    # Calculate size of each part
    part_size = math.ceil(file_size / num_parts)
    
    # Create output directory if it doesn't exist
    output_dir = f"{input_file}_parts"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        part_num = 1
        bytes_read = 0
        current_part = ""
        
        # Read the file line by line
        for line in f:
            current_part += line
            bytes_read += len(line.encode('utf-8'))
            
            # If we've read enough for this part, write it out
            if bytes_read >= part_size and part_num < num_parts:
                output_file = os.path.join(output_dir, f"part_{part_num}.txt")
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    out_f.write(current_part)
                
                # Reset for next part
                current_part = ""
                bytes_read = 0
                part_num += 1
        
        # Write the last part
        if current_part:
            output_file = os.path.join(output_dir, f"part_{part_num}.txt")
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(current_part)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a text file into equal parts')
    parser.add_argument('input_file', help='The text file to split')
    parser.add_argument('--parts', type=int, default=10, help='Number of parts to split into (default: 10)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        exit(1)
    
    split_file(args.input_file, args.parts)
    print(f"File split into {args.parts} parts in folder: {args.input_file}_parts") 