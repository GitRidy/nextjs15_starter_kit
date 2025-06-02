#!/usr/bin/env python3
"""
Purpose: Enhanced script to concatenate files with specified extensions from a folder and its subfolders
         into a single text file with formatted output.
Version: 1.01
Updated: 2025-06-02
Authors: JML with Claude Sonnet 4
"""

import os
import sys
import argparse
import codecs
from datetime import datetime
from pathlib import Path


def process_escape_sequences(input_string):
    """Decodes escape sequences like \\n into actual newline characters."""
    try:
        # Use 'unicode_escape' to interpret standard Python escape sequences
        return codecs.decode(input_string, 'unicode_escape')
    except Exception as e:
        print(f"Warning: Could not process escape sequences in separator '{input_string}': {e}. Using raw string.", file=sys.stderr)
        return input_string


def normalize_extensions(extensions):
    """
    Normalize a list of file extensions to ensure they start with a dot and are lowercase.
    
    Args:
        extensions (list): List of extensions (e.g., ['txt', '.py', 'MD'])
    
    Returns:
        list: Normalized extensions (e.g., ['.txt', '.py', '.md'])
    """
    normalized = []
    for ext in extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        normalized.append(ext.lower())
    return normalized


def find_matching_files(folder_path, extensions, levels):
    """
    Find all files matching the specified extensions in the given folder.
    
    Args:
        folder_path (Path): Path object for the folder to search
        extensions (list): List of extensions to match
        levels (int): Number of recursion levels (0 = current directory only)
    
    Returns:
        list: List of Path objects for matching files
    """
    matching_files = []
    
    def search_directory(current_path, current_level, max_level):
        """Recursively search directories up to the specified level."""
        try:
            for item in current_path.iterdir():
                if item.is_file():
                    if item.suffix.lower() in extensions:
                        matching_files.append(item)
                elif item.is_dir() and current_level < max_level:
                    search_directory(item, current_level + 1, max_level)
        except PermissionError as e:
            print(f"Warning: Permission denied when accessing {current_path}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Error searching {current_path}: {e}", file=sys.stderr)
    
    try:
        search_directory(folder_path, 0, levels)
    except Exception as e:
        print(f"Error searching for files: {e}", file=sys.stderr)
        return []
    
    # Sort files for consistent output
    matching_files.sort()
    return matching_files


def read_file_content(file_path):
    """
    Read content from a file with multiple encoding attempts.
    
    Args:
        file_path (Path): Path to the file to read
    
    Returns:
        tuple: (success: bool, content: str)
    """
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as infile:
                content = infile.read()
                if encoding != 'utf-8':
                    print(f"Successfully read {file_path.name} using {encoding} encoding")
                return True, content
        except UnicodeDecodeError:
            continue
        except IOError as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return False, f"[Error reading file: {e}]"
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {e}", file=sys.stderr)
            return False, f"[Unexpected error: {e}]"
    
    print(f"Warning: Could not read {file_path} with any supported encoding", file=sys.stderr)
    return False, f"[Could not decode file with supported encodings]"


def concat_files(folder_path, output_filename, extensions, sep1, sep2, levels):
    """
    Combines files in a specified folder into a single text file.

    Args:
        folder_path (str): The path to the folder containing the files.
        output_filename (str): The name for the combined output file.
        extensions (list): List of file extensions to filter by.
        sep1 (str): Separator to place under filename.
        sep2 (str): Separator to place between files.
        levels (int): Number of recursion levels.
    """
    
    # Convert to Path object for better handling
    root_path = Path(folder_path).resolve()
    
    if not root_path.exists():
        print(f"Error: Folder not found at path: {folder_path}", file=sys.stderr)
        return False
    
    if not root_path.is_dir():
        print(f"Error: The specified path is not a directory: {folder_path}", file=sys.stderr)
        return False
    
    # Prepare output path
    output_filepath = root_path / output_filename
    absolute_output_filepath = output_filepath.resolve()
    
    # Process separators
    processed_sep1 = process_escape_sequences(sep1)
    processed_sep2 = process_escape_sequences(sep2)
    
    # Normalize extensions
    normalized_extensions = normalize_extensions(extensions)
    ext_display = ", ".join(normalized_extensions)
    
    if levels == 0:
        search_mode = "in current directory only"
    else:
        search_mode = f"recursively up to {levels} level(s) deep"
    
    print(f"\nSearching for files with extensions [{ext_display}] {search_mode} in: {folder_path}")
    
    # Find matching files
    matching_files = find_matching_files(root_path, normalized_extensions, levels)
    
    # Filter out the output file itself
    matching_files = [f for f in matching_files if f.resolve() != absolute_output_filepath]
    
    if not matching_files:
        print(f"No files with extensions [{ext_display}] found in the specified location.")
        return False
    
    print(f"Found {len(matching_files)} file(s) to process")
    
    # Read content from each file
    processed_file_data = []  # Store tuples of (relative_path, content, read_success)
    
    for file_path in matching_files:
        try:
            relative_path = file_path.relative_to(root_path)
        except ValueError:
            relative_path = file_path  # Fallback to absolute path
        
        print(f"Reading: {relative_path}")
        success, content = read_file_content(file_path)
        processed_file_data.append((relative_path, content, success))
    
    # Write combined output
    if processed_file_data:
        print(f"\nCombining content and writing to: {output_filepath}")
        try:
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                # Use the refined format with customizable separators
                for i, (relative_path, content, success) in enumerate(processed_file_data):
                    # Write filename
                    outfile.write(f"{relative_path}\n")
                    outfile.write(f"{processed_sep1}\n")
                    
                    # Write content
                    outfile.write(content)
                    
                    # Ensure content ends with newline
                    if content and not content.endswith('\n'):
                        outfile.write('\n')
                    
                    # Write separator between files (except for the last one)
                    if i < len(processed_file_data) - 1:
                        outfile.write(f"{processed_sep2}\n\n")
                    else:
                        # Add final separator for consistency
                        outfile.write(f"{processed_sep2}\n")
            
            successful_reads = sum(1 for _, _, success in processed_file_data if success)
            print(f"Successfully combined {successful_reads}/{len(processed_file_data)} files into '{output_filename}'.")
            return True
            
        except IOError as e:
            print(f"Error writing to output file {output_filename}: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"An unexpected error occurred while writing the output file: {e}", file=sys.stderr)
            return False
    else:
        print("No files were found to process.")
        return False


def main():
    """Main function to handle command line arguments and run the script."""
    
    parser = argparse.ArgumentParser(
        description="Combine files from a folder into a single text file.",
        epilog="Examples:\n"
               "  Combine .py files recursively 2 levels deep: python %(prog)s --path \"/path/to/code\" --types py --levels 2\n"
               "  Combine multiple extensions: python %(prog)s --path \"/path/to/docs\" --types txt md py --levels 1\n"
               "  Custom separators: python %(prog)s --path \"/path\" --sep1 \"====\" --sep2 \"\\n---\\n\"\n"
               "  Use defaults (txt,md files in current dir): python %(prog)s",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--path",
        default=".",
        help="Path to the folder containing the files (default: current directory)",
        metavar="FOLDER_PATH"
    )
    
    parser.add_argument(
        "--filename",
        help="Name for the combined output file (default: concat_files_YYYY-MM-DD.txt)",
        metavar="OUTPUT_FILENAME"
    )
    
    parser.add_argument(
        "--types", 
        nargs='*',
        default=['txt', 'md'],
        help="File extension(s) to include (default: txt md)",
        metavar="EXT"
    )
    
    parser.add_argument(
        "--sep1",
        default="----",
        help="Separator string to place under filename (default: ----)",
        metavar="SEP_STRING"
    )
    
    parser.add_argument(
        "--sep2",
        default="====",
        help="Separator string to place between files (default: ====)",
        metavar="SEP_STRING"
    )
    
    parser.add_argument(
        "--levels",
        type=int,
        default=0,
        help="Number of recursion levels (0 = current directory only, default: 0)",
        metavar="N"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.levels < 0:
        print("Error: --levels must be 0 or greater", file=sys.stderr)
        sys.exit(1)
    
    # Handle empty types array
    if not args.types:
        print("Error: No file types specified. Use --types followed by extensions (e.g., --types txt md)", file=sys.stderr)
        sys.exit(1)

    # Set default output filename if not provided
    if args.filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_filename = f"concat_files_{today}.txt"
    else:
        output_filename = args.filename
        # Basic filename validation
        invalid_chars = '<>:"|?*'
        if any(char in output_filename for char in invalid_chars):
            print(f"Error: Output filename contains invalid characters: {invalid_chars}", file=sys.stderr)
            sys.exit(1)

    # Validate directory
    folder_path = Path(args.path)
    if not folder_path.exists():
        print(f"\nError: The specified path does not exist: '{args.path}'", file=sys.stderr)
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"\nError: The specified path is not a directory: '{args.path}'", file=sys.stderr)
        sys.exit(1)

    # Call the main function
    success = concat_files(
        folder_path=args.path,
        output_filename=output_filename,
        extensions=args.types,
        sep1=args.sep1,
        sep2=args.sep2,
        levels=args.levels
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()