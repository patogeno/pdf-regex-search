import os
import re
from PyPDF2 import PdfReader
import argparse
import sys

def search_pdfs(folder_path, regex_pattern, ignore_patterns):
    compiled_regex = re.compile(regex_pattern)
    compiled_ignore_patterns = [re.compile(pattern) for pattern in ignore_patterns]

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                
                # Check if the file should be ignored
                if any(ignore_pattern.search(file) for ignore_pattern in compiled_ignore_patterns):
                    continue
                
                try:
                    reader = PdfReader(full_path)
                    print(f"{full_path}:")
                    counter = 1
                    for page_num, page in enumerate(reader.pages, 1):
                        text = page.extract_text()
                        for match in compiled_regex.finditer(text):
                            print(f"{counter}. Page {page_num}, Position {match.start()}")
                            counter += 1
                    if counter == 1:
                        print("No matches found.")
                    print()  # Empty line for readability
                except Exception as e:
                    print(f"Error processing {full_path}: {str(e)}")
                    print()  # Empty line for readability

def main():
    parser = argparse.ArgumentParser(
        description="Search for regex patterns in PDFs within a specified folder and its subfolders.",
        epilog="""
Examples:
  python pdf_regex_search.py /path/to/pdfs "confidential" --ignore "draft" "old"
    This will search for the word "confidential" in all PDFs in the specified folder and its subfolders,
    ignoring any files with "draft" or "old" in their names.

  python pdf_regex_search.py /home/user/documents "\d{3}-\d{2}-\d{4}" --ignore "temp"
    This will search for a pattern matching a Social Security Number (XXX-XX-XXXX) in all PDFs,
    ignoring any files with "temp" in their names.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder_path", help="Path to the folder containing PDFs")
    parser.add_argument("regex_pattern", help="Regex pattern to search for")
    parser.add_argument("--ignore", nargs="*", default=[], help="Patterns to ignore in filenames")
    
    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    search_pdfs(args.folder_path, args.regex_pattern, args.ignore)

if __name__ == "__main__":
    main()