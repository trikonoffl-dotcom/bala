import fitz
import qrcode
from PIL import Image
import io
import os

def create_vcard_qr(data):
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:{data['last_name']};{data['first_name']};;;
FN:{data['first_name']} {data['last_name']}
ORG:
TITLE:{data['title']}
TEL;TYPE=WORK,VOICE:{data['phone_office']}
TEL;TYPE=CELL,VOICE:{data['phone_mobile']}
EMAIL;TYPE=PREF,INTERNET:{data['email']}
URL:{data['website']}
ADR;TYPE=WORK:;;{data['address']};;;;
END:VCARD"""
    
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(vcard_data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

def generate_card(template_path, data, style="Trikon"):
    doc = fitz.open(template_path)
    page = doc[1]  # Page 2 has the details in both PDFs
    
    text_color = (0, 0, 0)
    
    # Font Paths
    font_base = r"C:\Users\pabal\Documents\Businesscard"
    
    if style == "Trikon":
        # Register Poppins Fonts
        font_reg = os.path.join(font_base, "Poppins", "Poppins-Regular.ttf")
        font_bold = os.path.join(font_base, "Poppins", "Poppins-Bold.ttf")
        font_med = os.path.join(font_base, "Poppins", "Poppins-Medium.ttf")
        
        try:
             # Load Regular
             with open(font_reg, "rb") as f: fb_reg = f.read()
             ret = page.insert_font(fontname="pop-reg", fontbuffer=fb_reg)
             t_reg_name = ret if isinstance(ret, str) else "pop-reg"
             
             # Load Bold
             with open(font_bold, "rb") as f: fb_bold = f.read()
             ret = page.insert_font(fontname="pop-bold", fontbuffer=fb_bold)
             t_bold_name = ret if isinstance(ret, str) else "pop-bold"
             
             # Load Medium
             with open(font_med, "rb") as f: fb_med = f.read()
             ret = page.insert_font(fontname="pop-med", fontbuffer=fb_med)
             t_med_name = ret if isinstance(ret, str) else "pop-med"

        except Exception as e:
             # Fallback or raise
             raise ValueError(f"Failed to load Trikon fonts: {e}")

        # Insert Text using captured font names
        # Check if t_bold_name is valid string (it is now guaranteed)
        # Line is at approx y=41.3 to 42.1, Starts at x=32.58
        # Icons start at x=20.69. Blue line aligns with icons.
        # Name - Moved up 2pt (Baseline 26), Left Aligned to 21.15 (Align with blue line/icons)
        page.insert_text((21.15, 26), f"{data['first_name']} {data['last_name']}".upper(), fontsize=11, fontname=t_bold_name, color=text_color)
        # Title - Moved up 2pt (Baseline 36), Left Aligned to 21.15
        page.insert_text((21.15, 36), data['title'], fontsize=6, fontname=t_reg_name, color=text_color)
        
        # Address
        page.insert_text((34, 56), data['address_line1'], fontsize=6, fontname=t_med_name, color=text_color)
        page.insert_text((34, 64), data['address_line2'], fontsize=6, fontname=t_med_name, color=text_color)
        
        # Contact Blocks
        start_y = 75
        gap = 11
        page.insert_text((34, start_y), data['phone_mobile'], fontsize=6, fontname=t_med_name, color=text_color)
        page.insert_text((34, start_y + gap), data['email'], fontsize=6, fontname=t_med_name, color=text_color)
        page.insert_text((34, start_y + 2*gap), data['phone_office'], fontsize=6, fontname=t_med_name, color=text_color)
        page.insert_text((34, start_y + 3*gap), data['website'], fontsize=6, fontname=t_med_name, color=text_color)

        # QR Code (Trikon)
        # White Box Rect: (156.49, 35.16, 247.07, 125.73) -> Size 90.58
        # QR Size: 82.32
        # Centered X: 156.49 + (90.58 - 82.32)/2 = 160.62
        # Centered Y: 35.16 + (90.58 - 82.32)/2 = 39.29
        qr_x = 160.62
        qr_y = 39.29
        qr_s = 82.32
        qr_rect = fitz.Rect(qr_x, qr_y, qr_x + qr_s, qr_y + qr_s)
        page.insert_image(qr_rect, stream=create_vcard_qr(data))
    
    elif style == "Metaweb":
        # Register Montserrat Fonts (Static)
        # Verify these paths exist in C:\Users\pabal\Documents\Businesscard\Montserrat\static
        font_reg = os.path.join(font_base, "Montserrat", "static", "Montserrat-Regular.ttf")
        font_bold = os.path.join(font_base, "Montserrat", "static", "Montserrat-Bold.ttf")
        font_semi = os.path.join(font_base, "Montserrat", "static", "Montserrat-SemiBold.ttf")

        # Capture Return Values for insertion
        ret = page.insert_font(fontname="mont-reg", fontfile=font_reg)
        f_reg_name = ret if isinstance(ret, str) else "mont-reg"
        
        ret = page.insert_font(fontname="mont-bold", fontfile=font_bold)
        f_bold_name = ret if isinstance(ret, str) else "mont-bold"
        
        ret = page.insert_font(fontname="mont-semi", fontfile=font_semi)
        f_semi_name = ret if isinstance(ret, str) else "mont-semi"
        
        # Instantiate Font object for explicit width calculation
        with open(font_bold, "rb") as f:
            width_font = fitz.Font(fontbuffer=f.read())

        # Removed Redaction Rects (Templates are now blank)
        
        # Text
        # Name
        page.insert_text((18, 38), f"{data['first_name']}", fontsize=12, fontname=f_bold_name, color=text_color) 
        
        # Use font object to calculate length
        firstname_width = width_font.text_length(data['first_name'], fontsize=12)
        page.insert_text((18 + firstname_width + 4, 38), f"{data['last_name']}", fontsize=12, fontname=f_reg_name, color=text_color)
        
        # Title
        page.insert_text((19, 50), data['title'], fontsize=6, fontname=f_reg_name, color=text_color)
        
        # Contact
        page.insert_text((30, 74), data['phone_mobile'], fontsize=5, fontname=f_reg_name, color=text_color)
        page.insert_text((30, 88), data['phone_office'], fontsize=5, fontname=f_reg_name, color=text_color)
        page.insert_text((30, 103), data['email'], fontsize=5, fontname=f_reg_name, color=text_color)
        page.insert_text((30, 116), data['website'], fontsize=5, fontname=f_reg_name, color=text_color)
        page.insert_text((30, 129), data['address_line1'], fontsize=5, fontname=f_reg_name, color=text_color)
        page.insert_text((30, 137), data['address_line2'], fontsize=5, fontname=f_reg_name, color=text_color)

        # QR Code (Metaweb)
        # White Box Rect: (176.54, 71.67, 248.82, 143.95) -> Size 72.28
        # QR Size: 67.00
        # Centered X: 176.54 + (72.28 - 67.00)/2 = 179.18
        # Centered Y: 71.67 + (72.28 - 67.00)/2 = 74.31
        qr_x = 179.18
        qr_y = 74.31
        qr_s = 67.00
        qr_rect = fitz.Rect(qr_x, qr_y, qr_x + qr_s, qr_y + qr_s)
        page.insert_image(qr_rect, stream=create_vcard_qr(data))

    return doc.tobytes()
