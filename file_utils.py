import os

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