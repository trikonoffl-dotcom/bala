import streamlit as st
import os
import tools.business_card
import tools.welcome_aboard
import tools.dashboard

st.set_page_config(layout="wide", page_title="Trikon Dashboard", page_icon="⚙️")

# Global CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary: #000000;
        --accent: #0071E3;
        --bg: #F5F5F7;
        --sidebar-bg: #FFFFFF;
        --card-bg: #FFFFFF;
        --text: #1D1D1F;
        --text-secondary: #86868B;
        --border: #D2D2D7;
    }

    /* Main App Background */
    .stApp {
        background-color: var(--bg);
        color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Typography */
    h1, h2, h3, .stHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.022em !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 980px !important; /* Apple pill style */
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }

    .stButton>button:hover {
        background-color: #333333 !important;
        transform: scale(1.02) !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding-top: 2rem !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        background-color: white !important;
        padding: 0.5rem !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1) !important;
    }

    /* Cards Simulation */
    .stMetric {
        background: var(--card-bg);
        padding: 1.5rem !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0,0,0,0.02) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Header with Logo
with st.sidebar:
    logo_path = r"images/trikon-logo-blue.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_column_width=True)
    else:
        st.title("Trikon")
    st.markdown("<br>", unsafe_allow_html=True)

# Custom App-Style Navigation CSS
st.markdown("""
<style>
    /* Styled Radio as Vertical Menu */
    [data-testid="stSidebar"] .stRadio > div {
        background-color: transparent !important;
        gap: 8px !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background-color: #F5F5F7 !important;
        padding: 0.8rem 1rem !important;
        border-radius: 12px !important;
        border: 1px solid #D2D2D7 !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        display: block !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        color: #1D1D1F !important;
        font-weight: 500 !important;
    }
    
    /* Hover effect */
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #E2E2E7 !important;
        transform: translateX(4px) !important;
    }
    
    /* Active/Selected State - Streamlit marks the active radio specifically */
    [data-testid="stSidebar"] div[role="radiogroup"] > div[data-checked="true"] > label {
        background-color: var(--accent) !important;
        color: white !important;
        border-color: var(--accent) !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2) !important;
    }

    /* Hide the actual radio circle */
    [data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p {
        margin-left: 0px !important;
    }
    
    [data-testid="stSidebar"] .stRadio label div:first-child {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.markdown("<p style='font-weight: 600; font-size: 0.85rem; color: #86868B; text-transform: uppercase; letter-spacing: 0.05em; padding-left: 5px;'>Main Menu</p>", unsafe_allow_html=True)
tool = st.sidebar.radio("Select Tool", ["Dashboard", "Business Card Generator", "Welcome Aboard Generator", "Coming Soon"], label_visibility="collapsed")

if tool == "Dashboard":
    tools.dashboard.render()
elif tool == "Business Card Generator":
    tools.business_card.render()
elif tool == "Welcome Aboard Generator":
    tools.welcome_aboard.render()
elif tool == "Coming Soon":
    st.title("Coming Soon")
    st.write("More tools will be added here.")
