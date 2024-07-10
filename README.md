# PDF Regex Search

PDF Regex Search is a command-line tool that allows you to search for regex patterns within PDF files in a specified folder and its subfolders. It provides a flexible way to find specific content across multiple PDF documents efficiently.

## Features

- Search for regex patterns in multiple PDF files
- Case-insensitive regex matching by default, with an option for case-sensitive searches
- Include or exclude files based on regex patterns in filenames
- Save and load search configurations
- Verbose output option for detailed search results
- Progress bar to track search progress
- Dual logging system with detailed hourly logs and a summary of the latest search

## Installation

1. Ensure you have Python 3.6 or later installed on your system.

2. Clone this repository or download the source code:
   ```
   git clone https://github.com/patogeno/pdf-regex-search.git
   cd pdf-regex-search
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script using Python from the command line:

```
python main.py [folder_path] [regex_pattern] [options]
```

### Arguments

- `folder_path`: Path to the folder containing PDFs to search
- `regex_pattern`: Regular expression pattern to search for

### Options

- `-inc`, `--include`: Regex patterns to include in filenames
- `-i`, `--ignore`: Regex patterns to ignore in filenames
- `-v`, `--verbose`: Enable verbose output
- `-p`, `--use-previous`: Use arguments from the previous run
- `-f`, `--use-favorite`: Use a saved favorite configuration
- `-s`, `--save-favorite`: Save current arguments as a favorite configuration
- `--case-sensitive`: Enable case-sensitive matching (default: case-insensitive)

## Examples

1. Search for the word "confidential" (case-insensitive by default) in all PDFs in a folder, ignoring files with "draft" or "old" in their names:
   ```
   python main.py /path/to/pdfs "confidential" -i "draft|old"
   ```

2. Search for a Social Security Number pattern in PDFs that begin with "report", using verbose output and case-sensitive matching:
   ```
   python main.py /home/user/documents "\d{3}-\d{2}-\d{4}" -inc "^report" -v --case-sensitive
   ```

3. Use a previously saved configuration:
   ```
   python main.py -p
   ```

4. Save the current configuration as a favorite named "my_search":
   ```
   python main.py /path/to/pdfs "pattern" -s "my_search"
   ```

5. Use a saved favorite configuration:
   ```
   python main.py -f "my_search"
   ```

Note: All regex patterns (for content search, file inclusion, and file exclusion) are case-insensitive by default. Use the `--case-sensitive` flag to enable case-sensitive matching.

## Logs

The application maintains two types of log files:

1. Detailed Hourly Logs:
   - Filename format: `pdf_search_log_YYYYMMDD_HH.txt`
   - Contains comprehensive information about each search, including all file paths and timestamped entries
   - Logs are grouped by hour and appended to if multiple searches are performed in the same hour

2. Summary Log:
   - Filename: `pdf_search_latest.log`
   - Contains a summary of the most recent search, including:
     - Timestamp of the search
     - Arguments used for the search
     - Total number of PDF files found
     - Search results (matches found in files)
   - This log is overwritten with each new search, always containing the latest results

Both log files are stored in the same directory as the script.

## Contributing

Contributions to improve PDF Regex Search are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.