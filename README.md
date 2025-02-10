# BIR2316 PDF Splitter

This script extracts specific information from each page of a PDF file and splits it into separate PDF files named according to the extracted data.

## Features
- Reads an input PDF file.
- Extracts name, TIN, and date from each page.
- Saves each page as a separate PDF file with a structured filename.
- Supports optional start and end page parameters.

## Requirements
Install the required dependencies using:
```sh
pip install -r requirements.txt
```

## Usage
Run the script with:
```sh
python bir_2316_splitter.py <filename> [start_page] [end_page]
```

- `<filename>`: The PDF file to process.
- `[start_page]` (optional): The page number to start splitting from.
- `[end_page]` (optional): The page number to stop splitting at.

## Example
```sh
python bir_2316_splitter.py input.pdf 2 5
```
This will split pages 2 to 5 of `input.pdf`.

## Output
Extracted pages will be saved in a folder named after the input file.

## Build Executable
To create a standalone executable, use:
```sh
pyinstaller --onefile bir_2316_splitter.py
```

