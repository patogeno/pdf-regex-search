import argparse
from cli import setup_argparse
from config_manager import load_args, save_favorite, save_last_args
from pdf_searcher import search_pdfs

def main():
    parser = setup_argparse()
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
        parser.print_help()
        return

    search_pdfs(args)

if __name__ == "__main__":
    main()