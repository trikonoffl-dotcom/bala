import fitz  # pymupdf
import sys

def analyze_pdf(path, output_file):
    output_file.write(f"--- Analyzing: {path} ---\n")
    try:
        doc = fitz.open(path)
        for page_num, page in enumerate(doc):
            output_file.write(f"Page {page_num + 1} Rect: {page.rect}\n")
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" in b:
                    for line in b["lines"]:
                        for span in line["spans"]:
                            try:
                                text = span['text']
                                bbox = span['bbox']
                                font = span['font']
                                size = span['size']
                                output_file.write(f"Text: '{text}' | Font: {font} | Size: {size:.2f} | Rect: {bbox}\n")
                            except Exception as e:
                                output_file.write(f"Skipping span due to error: {e}\n")
    except Exception as e:
        output_file.write(f"Failed to process {path}: {e}\n")
    output_file.write("-" * 30 + "\n")

files = [
    r"C:\Users\pabal\Downloads\Kane Nelson.pdf",
    r"C:\Users\pabal\Downloads\Frank Ajmera New Meta.pdf"
]

with open("coords_output.txt", "w", encoding="utf-8") as f:
    for file in files:
        analyze_pdf(file, f)
