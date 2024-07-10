import os
from datetime import datetime

def get_log_filename():
    now = datetime.now()
    return f"pdf_search_log_{now.strftime('%Y%m%d_%H')}.txt"

def create_or_append_log_file(args, pdf_files):
    log_filename = get_log_filename()
    mode = 'a' if os.path.exists(log_filename) else 'w'
    
    with open(log_filename, mode) as log_file:
        log_file.write(f"\n{'='*50}\n")
        log_file.write(f"New search started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_filename, 'a') as log_file:
        log_file.write(f"[{timestamp}] {content}")