import sys
import os

try:
    import pypdf
except ImportError:
    print("pypdf not found. Please install it.")
    sys.exit(1)

def extract_text(pdf_path, output_file):
    output_file.write(f"--- Extracting text from: {pdf_path} ---\n")
    try:
        reader = pypdf.PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            output_file.write(f"Page {i+1}:\n")
            output_file.write(page.extract_text() + "\n")
            output_file.write("-" * 20 + "\n")
    except Exception as e:
        output_file.write(f"Error reading {pdf_path}: {e}\n")

files = [
    r"C:\Users\pabal\Downloads\Kane Nelson.pdf",
    r"C:\Users\pabal\Downloads\Frank Ajmera New Meta.pdf"
]

with open("pdf_content_utf8.txt", "w", encoding="utf-8") as f:
    for file in files:
        if os.path.exists(file):
            extract_text(file, f)
        else:
            f.write(f"File not found: {file}\n")
