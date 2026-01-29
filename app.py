import streamlit as st
import tools.business_card
import tools.welcome_aboard

st.set_page_config(layout="wide", page_title="Business Card Generator")

# Navigation
st.sidebar.title("Navigation")
tool = st.sidebar.radio("Select Tool", ["Business Card Generator", "Welcome Aboard Generator", "Coming Soon"])

if tool == "Business Card Generator":
    tools.business_card.render()
elif tool == "Welcome Aboard Generator":
    tools.welcome_aboard.render()
elif tool == "Coming Soon":
    st.title("Coming Soon")
    st.write("More tools will be added here.")
