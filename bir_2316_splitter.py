import os
import re
import sys
import PyPDF2
import threading

def extract_information(text):
    """Extract information from the given text."""

    name = re.sub(r"_+", "", re.sub(r"\s+", "",re.findall(r'.+,', text)[0][:-1]))
    lines = text.split('\n')

    # find the markers
    m = []

    for i, line in enumerate(lines):
        if re.search(r"0\s+0\s+0\s+0\s+0", line):
            m.append(i)

    n = m[1]-2
    if not re.sub(r"\s+", "", lines[n]).isdigit():
        n = n-1

    numbers = [re.sub(r"\s+", "", lines[m[0]-1]),
                  re.sub(r"\s+", "", lines[n-1]),
                  re.sub(r"\s+", "", lines[n])]
    tin = "".join(numbers)

    n = m[2]-1
    if not re.sub(r"\s+", "", lines[n]).isdigit():
        n = n-1

    numbers = [re.sub(r"\s+", "", lines[n-1]),
            re.sub(r"\s+", "", lines[n]),
            re.sub(r"\s+", "", lines[0])]
    monthyear = "".join(numbers)

    filename = ""+name+"_"+tin+"_"+monthyear
    pattern = r"(?:[A-ZÑ]+\s+)?[A-ZÑ]+_[0-9]{9}_[0-9]{8}"

    if not re.match(pattern, filename):
        print(f'Detected wrong filename: {filename}')
        return ""
    return filename

def process_page(reader, page_index, output):
    """Processes a single page in a separate thread."""
    page = reader.pages[page_index]
    text = page.extract_text() or ""

    try:
      page_filename = extract_information(text)

      if page_filename:
          writer = PyPDF2.PdfWriter()
          writer.add_page(page)
          output_path = os.path.join(output, f"{page_filename}.pdf")

          with open(output_path, "wb") as output_file:
              writer.write(output_file)
          print(f"Page {page_index + 1} saved as {page_filename}.pdf")
      else:
          print(f"Could not find name, TIN and date on page {page_index + 1}, skipping.")

    except Exception as e:
      print(f"Page {page_index + 1} Could not be saved: {e}")


def split_pdf(input_pdf, start_page=None, end_page=None):
    """Splits the specified PDF into multiple files."""
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found.")
        return

    output_path = input_pdf[:-3]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        print(f'{input_pdf} pages: {total_pages}')

        if start_page is None:
            start_page = 1
        if end_page is None:
            end_page = total_pages

        for i in range(start_page - 1, end_page):
            process_page(reader, i, output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename> [start_page] [end_page]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    start_page = int(sys.argv[2]) if len(sys.argv) > 2 else None
    end_page = int(sys.argv[3]) if len(sys.argv) > 3 else None

    split_pdf(input_pdf, start_page, end_page)
