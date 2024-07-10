import os
import re
from PyPDF2 import PdfReader
import argparse
import sys

def search_pdfs(folder_path, regex_pattern, ignore_patterns, verbose):
    compiled_regex = re.compile(regex_pattern)
    compiled_ignore_patterns = [re.compile(pattern) for pattern in ignore_patterns]
    matches_found = False

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                
                # Check if the file should be ignored
                if any(ignore_pattern.search(file) for ignore_pattern in compiled_ignore_patterns):
                    if verbose:
                        print(f"Ignoring file: {full_path}")
                    continue
                
                try:
                    reader = PdfReader(full_path)
                    file_matches = []
                    for page_num, page in enumerate(reader.pages, 1):
                        text = page.extract_text()
                        for match in compiled_regex.finditer(text):
                            file_matches.append(f"Page {page_num}, Position {match.start()}")
                    
                    if file_matches:
                        matches_found = True
                        print(f"{full_path}:")
                        for i, match in enumerate(file_matches, 1):
                            print(f"{i}. {match}")
                        print()  # Empty line for readability
                    elif verbose:
                        print(f"No matches found in {full_path}")
                        print()  # Empty line for readability
                except Exception as e:
                    if verbose:
                        print(f"Error processing {full_path}: {str(e)}")
                        print()  # Empty line for readability

    if not matches_found and verbose:
        print("No matches found in any files.")

def main():
    parser = argparse.ArgumentParser(
        description="Search for regex patterns in PDFs within a specified folder and its subfolders.",
        epilog="""
Examples:
  python pdf_regex_search.py /path/to/pdfs "confidential" --ignore "draft" "old"
    This will search for the word "confidential" in all PDFs in the specified folder and its subfolders,
    ignoring any files with "draft" or "old" in their names.

  python pdf_regex_search.py /home/user/documents "\d{3}-\d{2}-\d{4}" --ignore "temp" --verbose
    This will search for a pattern matching a Social Security Number (XXX-XX-XXXX) in all PDFs,
    ignoring any files with "temp" in their names, and showing verbose output.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder_path", help="Path to the folder containing PDFs")
    parser.add_argument("regex_pattern", help="Regex pattern to search for")
    parser.add_argument("--ignore", nargs="*", default=[], help="Patterns to ignore in filenames")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    search_pdfs(args.folder_path, args.regex_pattern, args.ignore, args.verbose)

if __name__ == "__main__":
    main()