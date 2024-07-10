from datetime import datetime

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