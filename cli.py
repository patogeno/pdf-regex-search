import argparse

def setup_argparse():
    parser = argparse.ArgumentParser(
        description="Search for regex patterns in PDFs within a specified folder and its subfolders.",
        epilog="""
Examples:
  python main.py /path/to/pdfs "confidential" -i "draft" "old" --ignore-mode contains
    This will search for the word "confidential" in all PDFs in the specified folder and its subfolders,
    ignoring any files with "draft" or "old" in their names.

  python main.py /home/user/documents "\d{3}-\d{2}-\d{4}" -inc "report" --include-mode beginswith -v
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
    
    return parser