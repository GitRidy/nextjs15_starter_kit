# File Concatenation Script

A powerful Python script that combines multiple files from a directory (and optionally its subdirectories) into a single text file with clean, consistent formatting. Perfect for creating documentation bundles, code reviews, or archiving related files.

Version: 1.0
Updated: 2025-05-29
Authors: JML with Claude Sonnet 4

## Features

- **Smart Defaults**: Works out-of-the-box for common use cases (txt/md files in current directory)
- **Flexible File Selection**: Filter by one or multiple file extensions
- **Precise Recursion Control**: Specify exact number of directory levels to search
- **Clean Output Format**: Consistent formatting with customizable separators
- **Robust Encoding Support**: Handles UTF-8, UTF-8-BOM, Latin-1, and CP1252 encodings
- **Smart File Exclusion**: Automatically excludes the output file from processing
- **Comprehensive Validation**: Input validation prevents common errors
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

No installation required! Just download the script. Requires Python 3.6+.

```bash
# Make the script executable (Unix/Linux/macOS)
chmod +x concat_files.py
```

## Quick Start

```bash
# Use defaults: txt/md files in current directory
python concat_files.py

# Combine Python files recursively 2 levels deep
python concat_files.py --types py --levels 2

# Combine multiple file types with custom output name
python concat_files.py --types py js html --levels 1 --filename my_code.txt
```

## Usage

### Basic Syntax
```bash
python concat_files.py [OPTIONS]
```

### Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--path` | Path to source folder | `.` (current directory) | `--path /path/to/files` |
| `--filename` | Output filename | `concat_files_YYYY-MM-DD.txt` | `--filename combined.txt` |
| `--types` | File extensions to include | `txt md` | `--types py js html` |
| `--levels` | Number of recursion levels | `0` (current dir only) | `--levels 2` |
| `--sep1` | Separator under filename | `----` | `--sep1 "====="` |
| `--sep2` | Separator between files | `====` | `--sep2 "\\n---\\n"` |

### Recursion Levels Explained
- `--levels 0`: Current directory only (default)
- `--levels 1`: Current directory + 1 level of subdirectories
- `--levels 2`: Current directory + 2 levels of subdirectories
- And so on...

## Output Format

The script produces clean, consistent output:

```
document1.txt
----
This is the content of document1.txt
Some more content here.
====

subfolder/document2.py
----
print("Hello from Python file")
# More Python code
====
```

## Examples

### Basic Examples

```bash
# Use all defaults (txt/md files in current directory)
python concat_files.py

# Combine Python files only
python concat_files.py --types py

# Custom output filename
python concat_files.py --filename my_docs.txt

# Search subdirectories (1 level deep)
python concat_files.py --levels 1
```

### Advanced Examples

```bash
# Multiple file types, 2 levels deep
python concat_files.py --types html css js --levels 2 --filename website_code.txt

# Custom separators with escape sequences
python concat_files.py --types log --sep1 "========" --sep2 "\\n=== NEXT FILE ===\\n"

# Specific directory with custom settings
python concat_files.py --path ./src --types py --levels 3 --filename source_code.txt

# Documentation bundle
python concat_files.py --path ./docs --types md rst txt --levels 2 --filename all_docs.txt
```

### Real-World Use Cases

```bash
# Code review bundle (Python project)
python concat_files.py --types py --levels 2 --filename code_review.txt

# Website source code
python concat_files.py --types html css js --levels 1 --filename website_source.txt

# Configuration backup
python concat_files.py --types conf cfg ini --filename config_backup.txt

# Documentation compilation
python concat_files.py --path ./documentation --types md txt --levels 3 --filename project_docs.txt

# Log file analysis
python concat_files.py --types log --sep2 "\\n\\n=== NEXT LOG ===\\n\\n" --filename all_logs.txt
```

## File Handling

### Encoding Support
The script automatically tries multiple encodings in order:
1. UTF-8 (most common)
2. UTF-8 with BOM
3. Latin-1 (Western European)
4. CP1252 (Windows)

If a file can't be read with any encoding, an error message is included in the output instead of the file content.

### File Processing
- **Extension matching**: Case-insensitive, handles extensions with or without dots
- **Path handling**: Cross-platform compatible, shows relative paths in output
- **Self-exclusion**: Output file automatically excluded from processing
- **Sorting**: Files processed in alphabetical order for consistent results

## Error Handling

The script gracefully handles various error conditions:

- **Invalid arguments**: Clear validation messages for all input parameters
- **Missing directories**: Informative error messages with proper exit codes
- **Permission errors**: Warnings for inaccessible files, continues with others
- **Encoding issues**: Tries multiple encodings, includes error message if all fail
- **Write errors**: Reports issues and exits cleanly
- **Empty results**: Clear feedback when no matching files found

## Default Behavior

When run without arguments, the script:
- Searches the current directory only (`--levels 0`)
- Includes `.txt` and `.md` files (`--types txt md`)
- Creates output file named `concat_files_YYYY-MM-DD.txt`
- Uses `----` under filenames and `====` between files

## Troubleshooting

### Common Issues

**"No files with extensions [.txt, .md] found"**
- Check that you have .txt or .md files in the current directory
- Use `--types` to specify different file extensions
- Use `--levels 1` or higher to search subdirectories

**"Error: No file types specified"**
- This happens when you use `--types` with no extensions
- Either remove `--types` (uses default txt/md) or specify extensions: `--types py js`

**"Permission denied"**
- Ensure you have read access to the source directory
- Ensure you have write access to the current directory
- Try specifying a different output location with `--filename`

**"Output filename contains invalid characters"**
- Avoid characters like `< > : " | ? *` in the filename
- Use simple filenames or let the script generate one automatically

### Getting Help

```bash
# Show detailed help and examples
python concat_files.py --help

# Test with a small directory first
python concat_files.py --types txt --levels 0
```

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## Validation Features

The script includes comprehensive input validation:
- ✅ Path existence and directory validation
- ✅ Non-negative recursion levels
- ✅ Non-empty file type specifications
- ✅ Output filename character validation
- ✅ Comprehensive error reporting

## Performance Notes

- Memory usage scales with total file content size
- Suitable for typical documentation and source code files
- For very large files (>100MB total), consider processing in smaller batches

## License

This script is provided as-is for educational and practical use. Feel free to modify and distribute as needed.

---

*Happy file concatenating! 🗂️*