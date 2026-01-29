import fitz
from collections import Counter

def get_bg_color(pdf_path, rect):
    doc = fitz.open(pdf_path)
    page = doc[1] # Page 2
    pix = page.get_pixmap(clip=rect)
    
    # Sample pixels
    pixels = []
    width, height = pix.width, pix.height
    for x in range(0, width, 5): # Sample every 5th pixel
        for y in range(0, height, 5):
            rgb = (pix.pixel(x, y)[0], pix.pixel(x, y)[1], pix.pixel(x, y)[2])
            pixels.append(rgb)
            
    most_common = Counter(pixels).most_common(1)[0][0]
    norm = (most_common[0]/255, most_common[1]/255, most_common[2]/255)
    print(f"File: {pdf_path}")
    print(f"Norm: {norm}")
    print("-" * 20)

files = [
    (r"C:\Users\pabal\Downloads\Kane Nelson.pdf", fitz.Rect(17, 14, 150, 40)),
    (r"C:\Users\pabal\Downloads\Frank Ajmera New Meta.pdf", fitz.Rect(18, 26, 170, 55))
]

with open("bg_colors_out.txt", "w") as f:
    import sys
    sys.stdout = f
    for f_path, r in files:
        get_bg_color(f_path, r)
