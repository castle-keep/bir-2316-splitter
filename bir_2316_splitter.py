import os
import re
import sys
import PyPDF2
import threading

def extract_information(text):
    """Extract information from the given text."""

    name = re.findall(r'.+,', text)[0][:-1]
    lines = text.split('\n')
    numbers = [re.sub(r"\s+", "", lines[2]),  # 3rd line
                  re.sub(r"\s+", "", lines[9]),  # 5th line
                  re.sub(r"\s+", "", lines[10])]
    tin = "".join(numbers)

    for i, line in enumerate(lines, start=1):
        if re.search( r"0\s+0\s+0\s+0\s+0", line):
            numbers = [re.sub(r"\s+", "", lines[i-3]),  # 3rd line
                  re.sub(r"\s+", "", lines[i-2]),
                  re.sub(r"\s+", "", lines[0])]
            monthyear = "".join(numbers)

    return ""+name+"_"+tin+"_"+monthyear

def process_page(reader, page_index, output):
    """Processes a single page in a separate thread."""
    page = reader.pages[page_index]
    text = page.extract_text() or ""

    try:
      extracted_info = extract_information(text)

      if extracted_info:
          writer = PyPDF2.PdfWriter()
          writer.add_page(page)
          output_path = os.path.join(output, f"{extracted_info}.pdf")

          with open(output_path, "wb") as output_file:
              writer.write(output_file)
          print(f"Page {page_index + 1} saved as {extracted_info}.pdf")
      else:
          print(f"No valid name, TIN, or date found on page {page_index + 1}, skipping.")

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

        if start_page is None:
            start_page = 1
        if end_page is None:
            end_page = total_pages

        # threads = []
        # for i in range(start_page - 1, end_page):
        #     thread = threading.Thread(target=process_page, args=(reader, i, output_path))
        #     thread.start()
        #     threads.append(thread)

        # for thread in threads:
        #     thread.join()

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
