import streamlit as st
import os
import tools.business_card
import tools.welcome_aboard
import tools.dashboard
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Trikon Dashboard", page_icon="⚙️")

# Global CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary: #000000;
        --accent: #0071E3;
        --bg: #F5F5F7;
        --sidebar-bg: rgba(255, 255, 255, 0.7); /* Glass Sidebar */
        --card-bg: rgba(255, 255, 255, 0.8); /* Glass Card */
        --text: #1D1D1F;
        --text-secondary: #86868B;
        --border: rgba(210, 210, 215, 0.4);
    }

    /* Modern Mesh Gradient Background */
    .stApp {
        background-color: #F5F5F7;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 113, 227, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(134, 134, 139, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(0, 113, 227, 0.03) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(134, 134, 139, 0.03) 0px, transparent 50%);
        color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: transparent !important;
    }

    /* Remove Sidebar Top Padding & Empty Header */
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }

    /* Bento Box Card System */
    .bento-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .bento-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
        border-color: rgba(0, 113, 227, 0.2);
    }

    /* Typography */
    h1, h2, h3, .stHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.03em !important;
    }

    p, span, label {
        letter-spacing: -0.01em !important;
    }

    /* Metric Cards Integration (Streamlit Native override) */
    /* Bento Box Card System - Overriding st.container(border=True) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: var(--card-bg) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 1.5rem !important;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Metric Cards Integration */
    [data-testid="stMetric"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
        animation: fadeIn 0.6s ease-out;
    }

    /* Re-styling Inputs for "App" Look */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 14px !important;
        border: 1px solid #D2D2D7 !important;
        padding: 0.7rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1) !important;
        background-color: white !important;
    }

    /* Custom Button Overhaul */
    .stButton>button {
        background: var(--accent) !important;
        color: white !important;
        border-radius: 14px !important; /* Squircle style */
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2) !important;
    }

    .stButton>button:hover {
        background: #005BBF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(0, 113, 227, 0.3) !important;
    }

    /* Adjust Padding of Main Content */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 50px !important;
    }

    /* Hide Streamlit Header gap */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Navigation Menu Styling Refinement */
    .nav-link-selected {
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Header with Logo
with st.sidebar:
    logo_path = r"images/trikon_logo.png"
    if os.path.exists(logo_path):
        # Center the logo with high-end padding
        st.markdown('<div style="display: flex; justify-content: center; padding: 20px 0;">', unsafe_allow_html=True)
        st.image(logo_path, width=200) 
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("Trikon")
    
    # option_menu for professional app-style navigation
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Business Card", "Welcome Aboard", "Settings"],
        icons=["house", "person-badge", "person-plus", "gear"], # Bootstrap icons used by option_menu
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"font-size": "1.1rem"}, # Removed specific color to allow inheritance
            "nav-link": {
                "font-size": "0.95rem", 
                "text-align": "left", 
                "margin": "4px", 
                "border-radius": "10px",
                "color": "#1D1D1F",
                "font-weight": "500"
            },
            "nav-link-selected": {"background-color": "#0071E3", "color": "white !important"},
        }
    )

# Routing
if selected == "Dashboard":
    tools.dashboard.render()
elif selected == "Business Card":
    tools.business_card.render()
elif selected == "Welcome Aboard":
    tools.welcome_aboard.render()
elif selected == "Settings":
    st.title("Settings")
    st.write("Settings and preferences will be added here.")
