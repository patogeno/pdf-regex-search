import os
import re
from PyPDF2 import PdfReader
import argparse
import sys

def match_pattern(filename, patterns, mode):
    for pattern in patterns:
        if mode == "beginswith" and filename.startswith(pattern):
            return True
        elif mode == "contains" and pattern in filename:
            return True
    return False

def filter_files(files, include_patterns, ignore_patterns, include_mode, ignore_mode):
    if include_patterns:
        files = [f for f in files if match_pattern(f, include_patterns, include_mode)]
    files = [f for f in files if not match_pattern(f, ignore_patterns, ignore_mode)]
    return files

def search_pdfs(folder_path, regex_pattern, include_patterns, ignore_patterns, include_mode, ignore_mode, verbose):
    compiled_regex = re.compile(regex_pattern)
    matches_found = False

    for root, _, files in os.walk(folder_path):
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        filtered_files = filter_files(pdf_files, include_patterns, ignore_patterns, include_mode, ignore_mode)
        
        for file in filtered_files:
            full_path = os.path.join(root, file)
            
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
  python pdf_regex_search.py /path/to/pdfs "confidential" --ignore "draft" "old" --ignore-mode contains
    This will search for the word "confidential" in all PDFs in the specified folder and its subfolders,
    ignoring any files with "draft" or "old" in their names.

  python pdf_regex_search.py /home/user/documents "\d{3}-\d{2}-\d{4}" --include "report" --include-mode beginswith --verbose
    This will search for a pattern matching a Social Security Number (XXX-XX-XXXX) in PDFs that begin with "report",
    showing verbose output.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder_path", help="Path to the folder containing PDFs")
    parser.add_argument("regex_pattern", help="Regex pattern to search for")
    parser.add_argument("--include", nargs="*", default=[], help="Patterns to include in filenames")
    parser.add_argument("--ignore", nargs="*", default=[], help="Patterns to ignore in filenames")
    parser.add_argument("--include-mode", choices=["beginswith", "contains"], default="contains",
                        help="Mode for include patterns (default: contains)")
    parser.add_argument("--ignore-mode", choices=["beginswith", "contains"], default="contains",
                        help="Mode for ignore patterns (default: contains)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    search_pdfs(args.folder_path, args.regex_pattern, args.include, args.ignore, 
                args.include_mode, args.ignore_mode, args.verbose)

if __name__ == "__main__":
    main()