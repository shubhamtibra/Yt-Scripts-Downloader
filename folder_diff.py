#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
from pathlib import Path

def get_all_files(folder):
    """Get all files from a folder and its subdirectories.
    Returns a list of paths relative to the input folder."""
    files = []
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            # Skip hidden files
            if filename.startswith('.'):
                continue
            # Get full path
            full_path = os.path.join(root, filename)
            # Get relative path
            rel_path = os.path.relpath(full_path, folder)
            files.append(filename)
    return files

def find_unique_files(folder1, folder2):
    """Find files that are in folder1 but not in folder2"""
    files1 = set(get_all_files(folder1))
    files2 = set(get_all_files(folder2))
    
    # Files unique to folder1
    unique_to_folder1 = files1 - files2
    
    return unique_to_folder1

def copy_unique_files(source_folder, unique_files, output_folder):
    """Copy unique files from source_folder to output_folder, preserving directory structure"""
    for file_path in unique_files:
        # Source file path
        source_file = os.path.join(source_folder, file_path)
        
        # Destination file path
        dest_file = os.path.join(output_folder, file_path)
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        
        # Copy the file
        shutil.copy2(source_file, dest_file)
        print(f"Copied: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Find files in folder1 that don't exist in folder2 and copy them to an output folder")
    parser.add_argument("folder1", help="First input folder")
    parser.add_argument("folder2", help="Second input folder")
    parser.add_argument("output_folder", help="Output folder for unique files")
    
    args = parser.parse_args()
    
    folder1 = args.folder1
    folder2 = args.folder2
    output_folder = args.output_folder
    
    # Validate input folders
    if not os.path.isdir(folder1):
        print(f"Error: '{folder1}' is not a valid directory.")
        sys.exit(1)
    
    if not os.path.isdir(folder2):
        print(f"Error: '{folder2}' is not a valid directory.")
        sys.exit(1)
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find unique files in folder1 (not in folder2)
    print(f"Finding files in '{folder1}' that don't exist in '{folder2}'...")
    unique_to_folder1 = find_unique_files(folder1, folder2)
    
    if not unique_to_folder1:
        print(f"No unique files found in '{folder1}'.")
    else:
        print(f"Found {len(unique_to_folder1)} unique files in '{folder1}'.")
        
        # Copy unique files to output folder
        copy_unique_files(folder1, unique_to_folder1, output_folder)
        print(f"Copied {len(unique_to_folder1)} files to '{output_folder}'.")
    
    # Find unique files in folder2 (not in folder1)
    print(f"\nFinding files in '{folder2}' that don't exist in '{folder1}'...")
    unique_to_folder2 = find_unique_files(folder2, folder1)
    
    if not unique_to_folder2:
        print(f"No unique files found in '{folder2}'.")
    else:
        print(f"Found {len(unique_to_folder2)} unique files in '{folder2}'.")
        
        # Copy unique files to output folder
        copy_unique_files(folder2, unique_to_folder2, output_folder)
        print(f"Copied {len(unique_to_folder2)} files to '{output_folder}'.")
    
    total_files = len(unique_to_folder1) + len(unique_to_folder2)
    print(f"\nOperation complete! Copied a total of {total_files} unique files to '{output_folder}'.")

if __name__ == "__main__":
    main() 