import os
import re

def match_pattern(filename, patterns, case_sensitive=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    return any(re.search(pattern, filename, flags) for pattern in patterns)

def filter_files(files, include_patterns, ignore_patterns, case_sensitive=False):
    if include_patterns:
        files = [f for f in files if match_pattern(os.path.basename(f), include_patterns, case_sensitive)]
    files = [f for f in files if not match_pattern(os.path.basename(f), ignore_patterns, case_sensitive)]
    return files

def get_pdf_files(folder_path, include_patterns, ignore_patterns, case_sensitive=False):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        pdf_files.extend([os.path.join(root, f) for f in files if f.lower().endswith('.pdf')])
    return filter_files(pdf_files, include_patterns, ignore_patterns, case_sensitive)