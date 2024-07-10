import os
import re

def match_pattern(filename, patterns):
    return any(re.search(pattern, filename) for pattern in patterns)

def filter_files(files, include_patterns, ignore_patterns):
    if include_patterns:
        files = [f for f in files if match_pattern(os.path.basename(f), include_patterns)]
    files = [f for f in files if not match_pattern(os.path.basename(f), ignore_patterns)]
    return files

def get_pdf_files(folder_path, include_patterns, ignore_patterns):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        pdf_files.extend([os.path.join(root, f) for f in files if f.lower().endswith('.pdf')])
    return filter_files(pdf_files, include_patterns, ignore_patterns)