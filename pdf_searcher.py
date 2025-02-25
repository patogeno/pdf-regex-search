import re
from PyPDF2 import PdfReader
from file_utils import get_pdf_files
from logger import create_detailed_log_file, append_to_detailed_log, create_summary_log, append_to_summary_log, finalize_logs
import sys

def update_progress(current, total):
    percent = int(current / total * 100)
    bar_length = 50
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent}% Complete')
    sys.stdout.flush()

def search_pdfs(args):
    if not args.folder_path or not args.regex_pattern:
        print("Error: Both folder_path and regex_pattern are required for the search.")
        return

    flags = 0 if args.case_sensitive else re.IGNORECASE
    compiled_regex = re.compile(args.regex_pattern, flags)
    matches_found = False
    
    pdf_files = get_pdf_files(args.folder_path, args.include, args.ignore, args.case_sensitive)
    total_files = len(pdf_files)
    
    print("Arguments used for the search:")
    for key, value in vars(args).items():
        if value is not None and value != []:
            print(f"{key}: {value}")
    print()

    detailed_log_filename = create_detailed_log_file(args, pdf_files)
    create_summary_log(args, total_files)
    print(f"Found {total_files} PDF files to search.")
    print(f"Detailed log file: {detailed_log_filename}")
    print(f"Summary log file: pdf_search_latest.log")
    
    user_input = input("Do you want to continue with the search? (y/n): ").strip().lower()
    if user_input != 'y':
        print("Search cancelled by user.")
        append_to_detailed_log(detailed_log_filename, "Search cancelled by user before processing files.\n")
        append_to_summary_log("Search cancelled by user before processing files.\n")
        return
    
    print("Starting search...")
    append_to_detailed_log(detailed_log_filename, "Starting search...\n")
    
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
                append_to_detailed_log(detailed_log_filename, result)
                append_to_summary_log(result)
            elif args.verbose:
                result = f"No matches found in {full_path}\n"
                print(result)
                append_to_detailed_log(detailed_log_filename, result)
                append_to_summary_log(result)
        except Exception as e:
            if args.verbose:
                error_msg = f"Error processing {full_path}: {str(e)}\n"
                print(error_msg)
                append_to_detailed_log(detailed_log_filename, error_msg)
                append_to_summary_log(error_msg)
        
        update_progress(i, total_files)
    
    print()  # Move to a new line after the progress bar
    finalize_logs(detailed_log_filename, matches_found)
    if not matches_found:
        print("No matches found in any files.")