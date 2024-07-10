import os
import re

def match_pattern(filename, patterns, mode):
    for pattern in patterns:
        if mode == "full":
            if re.search(pattern, filename):
                return True
        elif mode == "beginswith":
            if re.match(f"^{pattern}", filename):
                return True
    return False

def filter_files(files, include_patterns, ignore_patterns, include_mode, ignore_mode):
    if include_patterns:
        files = [f for f in files if match_pattern(os.path.basename(f), include_patterns, include_mode)]
    files = [f for f in files if not match_pattern(os.path.basename(f), ignore_patterns, ignore_mode)]
    return files

def get_pdf_files(folder_path, include_patterns, ignore_patterns, include_mode, ignore_mode):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        pdf_files.extend([os.path.join(root, f) for f in files if f.lower().endswith('.pdf')])
    return filter_files(pdf_files, include_patterns, ignore_patterns, include_mode, ignore_mode)