import os
import re
from PyPDF2 import PdfReader
import argparse
import sys
import time
from datetime import datetime
import json

CONFIG_FILE = 'pdf_search_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'last_args': {}, 'favorites': {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def save_last_args(args):
    config = load_config()
    args_dict = vars(args)
    # Exclude certain arguments from being saved
    exclude_args = ['use_previous', 'use_favorite', 'save_favorite']
    config['last_args'] = {k: v for k, v in args_dict.items() if k not in exclude_args and v is not None}
    save_config(config)

def load_args(args, use_previous, use_favorite):
    config = load_config()
    if use_previous:
        loaded_args = config.get('last_args', {})
    elif use_favorite:
        loaded_args = config.get('favorites', {}).get(use_favorite, {})
    else:
        return args

    # Update args with loaded values, but don't override explicitly provided args
    for key, value in loaded_args.items():
        if getattr(args, key) is None or (isinstance(getattr(args, key), list) and not getattr(args, key)):
            setattr(args, key, value)
    
    return args

def save_favorite(name, args):
    config = load_config()
    args_dict = vars(args)
    # Exclude certain arguments from being saved
    exclude_args = ['use_previous', 'use_favorite', 'save_favorite']
    config['favorites'][name] = {k: v for k, v in args_dict.items() if k not in exclude_args and v is not None}
    save_config(config)
    print(f"Saved current arguments as favorite '{name}'")

def match_pattern(filepath, patterns, mode):
    filename = os.path.basename(filepath)
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

def get_pdf_files(folder_path, include_patterns, ignore_patterns, include_mode, ignore_mode):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        pdf_files.extend([os.path.join(root, f) for f in files if f.lower().endswith('.pdf')])
    return filter_files(pdf_files, include_patterns, ignore_patterns, include_mode, ignore_mode)

def update_progress(current, total):
    percent = int(current / total * 100)
    bar_length = 50
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent}% Complete')
    sys.stdout.flush()

def create_log_file(args, pdf_files):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"pdf_search_log_{timestamp}.txt"
    with open(log_filename, 'w') as log_file:
        log_file.write("Arguments used for the search:\n")
        for key, value in vars(args).items():
            if value is not None and value != []:
                log_file.write(f"{key}: {value}\n")
        log_file.write(f"\nFound {len(pdf_files)} PDF files to search:\n")
        for file in pdf_files:
            log_file.write(f"{file}\n")
        log_file.write("\nSearch Results:\n")
    return log_filename

def append_to_log(log_filename, content):
    with open(log_filename, 'a') as log_file:
        log_file.write(content)

def search_pdfs(args):
    if not args.folder_path or not args.regex_pattern:
        print("Error: Both folder_path and regex_pattern are required for the search.")
        return

    compiled_regex = re.compile(args.regex_pattern)
    matches_found = False
    
    pdf_files = get_pdf_files(args.folder_path, args.include, args.ignore, args.include_mode, args.ignore_mode)
    total_files = len(pdf_files)
    
    print("Arguments used for the search:")
    for key, value in vars(args).items():
        if value is not None and value != []:
            print(f"{key}: {value}")
    print()

    log_filename = create_log_file(args, pdf_files)
    print(f"Found {total_files} PDF files to search.")
    print(f"Log file created: {log_filename}")
    
    user_input = input("Do you want to continue with the search? (y/n): ").strip().lower()
    if user_input != 'y':
        print("Search cancelled by user.")
        append_to_log(log_filename, "\nSearch cancelled by user before processing files.\n")
        return
    
    print("Starting search...")
    append_to_log(log_filename, "\nStarting search...\n")
    
    for i, full_path in enumerate(pdf_files, 1):
        try:
            reader = PdfReader(full_path)
            file_matches = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                for match in compiled_regex.finditer(text):
                    file_matches.append(f"Page {page_num}, Position {match.start()}")
            
            if file_matches:
                matches_found = True
                result = f"\n{full_path}:\n"
                for j, match in enumerate(file_matches, 1):
                    result += f"{j}. {match}\n"
                result += "\n"
                print(result)
                append_to_log(log_filename, result)
            elif args.verbose:
                result = f"\nNo matches found in {full_path}\n\n"
                print(result)
                append_to_log(log_filename, result)
        except Exception as e:
            if args.verbose:
                error_msg = f"\nError processing {full_path}: {str(e)}\n\n"
                print(error_msg)
                append_to_log(log_filename, error_msg)
        
        update_progress(i, total_files)
    
    print()  # Move to a new line after the progress bar
    if not matches_found:
        no_matches_msg = "No matches found in any files.\n"
        print(no_matches_msg)
        append_to_log(log_filename, no_matches_msg)

def main():
    parser = argparse.ArgumentParser(
        description="Search for regex patterns in PDFs within a specified folder and its subfolders.",
        epilog="""
Examples:
  python pdf_regex_search.py /path/to/pdfs "confidential" -i "draft" "old" --ignore-mode contains
    This will search for the word "confidential" in all PDFs in the specified folder and its subfolders,
    ignoring any files with "draft" or "old" in their names.

  python pdf_regex_search.py /home/user/documents "\d{3}-\d{2}-\d{4}" -inc "report" --include-mode beginswith -v
    This will search for a pattern matching a Social Security Number (XXX-XX-XXXX) in PDFs that begin with "report",
    showing verbose output.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder_path", nargs='?', help="Path to the folder containing PDFs")
    parser.add_argument("regex_pattern", nargs='?', help="Regex pattern to search for")
    parser.add_argument("-inc", "--include", nargs="*", default=[], help="Patterns to include in filenames")
    parser.add_argument("-i", "--ignore", nargs="*", default=[], help="Patterns to ignore in filenames")
    parser.add_argument("--include-mode", choices=["beginswith", "contains"], default="contains",
                        help="Mode for include patterns (default: contains)")
    parser.add_argument("--ignore-mode", choices=["beginswith", "contains"], default="contains",
                        help="Mode for ignore patterns (default: contains)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-p", "--use-previous", action="store_true", help="Use arguments from the previous run")
    parser.add_argument("-f", "--use-favorite", help="Use a saved favorite configuration")
    parser.add_argument("-s", "--save-favorite", help="Save current arguments as a favorite configuration")
    
    args = parser.parse_args()
    
    # Load previous or favorite args if requested
    args = load_args(args, args.use_previous, args.use_favorite)
    
    # Save as favorite if requested
    if args.save_favorite:
        save_favorite(args.save_favorite, args)
    
    # Save current args as last used
    save_last_args(args)
    
    # If no arguments are provided and not using previous/favorite, print help and exit
    if not args.folder_path and not args.regex_pattern and not args.use_previous and not args.use_favorite:
        parser.print_help(sys.stderr)
        sys.exit(1)

    search_pdfs(args)

if __name__ == "__main__":
    main()