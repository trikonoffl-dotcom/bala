import fitz

def analyze(path):
    output = []
    doc = fitz.open(path)
    page = doc[0]
    page_rect = page.rect
    output.append(f"Page Size: {page_rect}")
    
    output.append("\n--- Drawings (Candidates for Photo Box) ---")
    paths = page.get_drawings()
    for p in paths:
        r = p['rect']
        # Filter out full page backgrounds
        if abs(r.width - page_rect.width) < 10 and abs(r.height - page_rect.height) < 10:
            continue
            
        output.append(f"Rect: {r}, Fill: {p['fill']}, Color: {p['color']}, Type: {p['type']}")

    with open("analysis.txt", "w") as f:
        f.write("\n".join(output))

analyze(r"C:\Users\pabal\Documents\Businesscard\Templates\welcome aboard - Without name.pdf")
