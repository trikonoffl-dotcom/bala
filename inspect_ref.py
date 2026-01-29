import fitz

def analyze(path):
    output = []
    doc = fitz.open(path)
    page = doc[0]
    
    output.append("\n--- Text Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    output.append(f"Text: '{s['text']}' @ {s['bbox']} Font: {s['font']} Size: {s['size']} Color: {s['color']}")

    with open("analysis_ref.txt", "w") as f:
        f.write("\n".join(output))

analyze(r"C:\Users\pabal\Documents\Businesscard\Templates\welcome aboard.pdf")
