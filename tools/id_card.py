import streamlit as st
import os
import requests
import io
import fitz
import datetime
from PIL import Image, ImageOps

# Photoroom API Key (Live)
PHOTOROOM_API_KEY = "sk_pr_default_badcd4bd9dd67dee9a1bbc4912c109f6d21a7cb1"

def remove_background(image_bytes):
    """Call Photoroom API to remove background."""
    url = "https://sdk.photoroom.com/v1/segment"
    headers = {
        "x-api-key": PHOTOROOM_API_KEY,
        "Accept": "image/png"
    }
    files = {
        "image_file": ("image.jpg", image_bytes, "image/jpeg")
    }
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.content
    elif response.status_code == 402:
        st.error("💡 **Photoroom API Quota Exhausted**: You've used all your AI background removal credits. Please upgrade your plan at [photoroom.com](https://app.photoroom.com/api-dashboard) or **uncheck** 'AI Background Removal' to proceed with the original photo.")
        return None
    else:
        st.error(f"Background removal failed: {response.status_code} - {response.text}")
        return None

def render():
    st.title("AI ID Card Generator")
    st.markdown("<p style='color: #6B7280; font-size: 1.15rem; font-weight: 400; letter-spacing: -0.01em;'>AI-powered ID cards with automatic background removal and backside details.</p>", unsafe_allow_html=True)

    # Office Addresses
    offices = {
        "Chennai": "Centre Point 3 , 7th Floor\n2/4 Mount Ponnamallee High Road\nManapakkam, Porur, Chennai 600089",
        "Ahmedabad": "COLONNADE-2, 1105, 11th Floor\nbehind Rajpath Rangoli Road\nBodakdev, Ahmedabad, Gujarat 380059"
    }

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("<h4 style='font-weight: 600; font-size: 1.25rem; margin-bottom: 1.5rem;'>Front Side Details</h4>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<p style='font-weight: 500; font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;'>Basic Identity</p>", unsafe_allow_html=True)
            first_name = st.text_input("First Name", "Bragadeesh")
            last_name = st.text_input("Last Name", "Sundararajan")
            title = st.text_input("Job Title", "AI Prompt Engineer")
        
        with st.container(border=True):
            st.markdown("<p style='font-weight: 500; font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;'>System Info</p>", unsafe_allow_html=True)
            id_number = st.text_input("ID Number", "TRC00049")
            doj = st.date_input("Joining Date", datetime.date(2025, 11, 17))
        
        st.markdown("<h4 style='font-weight: 600; font-size: 1.25rem; margin-top: 2rem; margin-bottom: 1.5rem;'>Back Side Details</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<p style='font-weight: 500; font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;'>Emergency & Health</p>", unsafe_allow_html=True)
            emergency_no = st.text_input("Emergency Number", "9566191956")
            blood_group = st.selectbox("Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"], index=0)
            
            st.markdown("<p style='font-weight: 500; font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1rem; margin-bottom: 0.5rem;'>Office Address</p>", unsafe_allow_html=True)
            office_choice = st.selectbox("Select Office", list(offices.keys()))
            office_address = st.text_area("Edit Address", offices[office_choice], height=100)
        
        with st.container(border=True):
            st.markdown("<p style='font-weight: 500; font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;'>Profile Media</p>", unsafe_allow_html=True)
            photo_file = st.file_uploader("Upload Portrait Photo", type=["jpg", "jpeg", "png"])
            remove_bg = st.checkbox("AI Background Removal (Photoroom)", value=True)

        generate_btn = st.button("Generate ID Card", use_container_width=True)

    with col2:
        st.markdown("<h4 style='font-weight: 600; font-size: 1.25rem; margin-bottom: 1.5rem;'>Final Preview</h4>")
        
        if not (generate_btn and photo_file):
             with st.container(border=True):
                st.info("Upload a photo and fill in the details to generate the card.", icon="🪪")

        if generate_btn and photo_file:
            photo_bytes = photo_file.read()
            
            with st.spinner("AI is processing image and generating PDF..."):
                if remove_bg:
                    processed_photo = remove_background(photo_bytes)
                else:
                    processed_photo = photo_bytes
                
            if processed_photo:
                try:
                    possible_paths = [
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Templates", "idcard", "id_card_empty.pdf"),
                        os.path.join(os.getcwd(), "Templates", "idcard", "id_card_empty.pdf"),
                        r"C:\Users\pabal\Documents\Businesscard\Templates\idcard\id_card_empty.pdf"
                    ]
                    
                    template_path = next((p for p in possible_paths if os.path.exists(p)), None)
                    
                    if template_path:
                        doc = fitz.open(template_path)
                        
                        # --- FONT REGISTRATION ---
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        font_dir = os.path.join(current_dir, "..", "fonts", "Rubik", "static")
                        if not os.path.exists(font_dir):
                            font_dir = r"C:\Users\pabal\Documents\Businesscard\fonts\Rubik\static"
                        
                        fonts_map = {
                            "ru-bold": os.path.join(font_dir, "Rubik-Bold.ttf"),
                            "ru-reg": os.path.join(font_dir, "Rubik-Regular.ttf"),
                            "ru-semi": os.path.join(font_dir, "Rubik-SemiBold.ttf"),
                            "ru-italic": os.path.join(font_dir, "Rubik-Italic.ttf")
                        }
                        
                        # FRONT PAGE (Index 0)
                        page0 = doc[0]
                        for name, path in fonts_map.items():
                            if os.path.exists(path):
                                page0.insert_font(fontname=name, fontfile=path)
                        
                        blue_text = (18/255, 34/255, 66/255)
                        white_text = (1, 1, 1)
                        
                        # Front Text Insertion
                        page0.insert_text((14.8, 148), first_name.upper(), fontsize=15, fontname="ru-bold", color=blue_text)
                        page0.insert_text((15.0, 168), last_name.upper(), fontsize=11, fontname="ru-reg", color=blue_text)
                        page0.insert_text((15.5, 183), title, fontsize=8, fontname="ru-reg", color=blue_text)
                        
                        date_str = doj.strftime("%d-%m-%Y")
                        page0.insert_text((15.1, 196), f"D.O.J:  {date_str}", fontsize=8, fontname="ru-bold", color=blue_text)
                        page0.insert_text((15.6, 226), f"ID Number: {id_number}", fontsize=10, fontname="ru-reg", color=white_text)
                        
                        # Front Photo
                        photo_rect = fitz.Rect(15, 28, 110, 126)
                        # The original code had PIL image processing here, but the instruction implies direct stream usage.
                        # If further image manipulation (e.g., cropping, resizing) is needed, PIL should be re-integrated.
                        page0.insert_image(photo_rect, stream=processed_photo)
                        
                        # BACK PAGE (Index 1)
                        if len(doc) > 1:
                            page1 = doc[1]
                            for name, path in fonts_map.items():
                                if os.path.exists(path):
                                    page1.insert_font(fontname=name, fontfile=path)
                            
                            # Backside Text
                            page1.insert_text((20, 93), f"Emergency Number: {emergency_no}", fontsize=7, fontname="ru-reg", color=white_text)
                            page1.insert_text((49, 106), f"Blood Group: {blood_group}", fontsize=7, fontname="ru-reg", color=white_text)
                            
                            # Backside Title
                            page1.insert_text((20, 167), "Trikon Telesoft Private Limited", fontsize=7, fontname="ru-semi", color=white_text)
                            
                            # Address Multi-line
                            addr_lines = office_address.split("\n")
                            y_offset = 173
                            for line in addr_lines:
                                page1.insert_text((15, y_offset), line.strip(), fontsize=6.5, fontname="ru-reg", color=white_text)
                                y_offset += 8.5
                        
                        # Log to Supabase
                        import utils.db as db
                        db.log_generation(tool="ID Card", name=f"{first_name} {last_name}", metadata={"id": id_number})

                        # Preview (Front & Back)
                        st.markdown("### Front Side")
                        pix0 = page0.get_pixmap(matrix=fitz.Matrix(3, 3))
                        st.image(pix0.tobytes("png"), use_column_width=True)
                        
                        if len(doc) > 1:
                            st.markdown("### Back Side")
                            pix1 = doc[1].get_pixmap(matrix=fitz.Matrix(3, 3))
                            st.image(pix1.tobytes("png"), use_column_width=True)
                        
                        pdf_bytes = doc.write()
                        st.download_button(
                            label="Download Full ID Card (2 Pages)",
                            data=pdf_bytes,
                            file_name=f"ID_Card_{id_number}.pdf",
                            mime="application/pdf"
                        )
                        doc.close()
                    else:
                        st.error(f"Template not found. Searched: {possible_paths}")
                except Exception as e:
                    st.error(f"Error: {e}")
