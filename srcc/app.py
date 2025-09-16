# src/app.py
import streamlit as st
from pathlib import Path
import base64
import os

# ========== CONFIG ========== #
st.set_page_config(page_title="Risk Analyst Hub", layout="wide", initial_sidebar_state="expanded")
STATIC_DIR = Path(__file__).parent / "static"
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# ========== CHARGER LES STYLES CSS ========== #
def load_styles():
    css_files = [
        "style.css", "sidebar.css", "about.css", "note_ai.css",
        "agent_card.css", "main_area.css", "main_chat_input.css",
        "step_indicator.css"
    ]
    for css_file in css_files:
        css_path = STATIC_DIR / css_file
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ========== CHARGER UN HTML ========== #
def load_html(filename):
    html_path = STATIC_DIR / filename
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ========== LOGO EN BASE64 POUR SIDEBAR ========== #
def load_logo():
    logo_path = STATIC_DIR / "assets" / "logo_lgi.png"
    if logo_path.exists():
        with open(logo_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return None


# ========== UI SIDEBAR ========== #
def sidebar():
    # Charger le CSS spécifique à la sidebar
    sidebar_css_path = STATIC_DIR / "sidebar.css"
    if sidebar_css_path.exists():
        with open(sidebar_css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Charger le logo
    logo_base64 = load_logo()
    
    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
<div class='sidebar-logo-block'>
    <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo" />
    <div class='sidebar-title'>Risk Analyst</div>
</div>
""", unsafe_allow_html=True)
# ========== UI PRINCIPALE ========== #
def main_ui():
    st.title("📊 AI Assistant for Risk Analysis")
    st.markdown("Welcome to your AI-enhanced risk assessment workspace.")

    html = load_html("static_feature_card.html")
    st.markdown(html, unsafe_allow_html=True)

    with st.expander("ℹ️ About this App", expanded=False):
        about_html = load_html("about.html")
        st.markdown(about_html, unsafe_allow_html=True)

# ========== MAIN ========== #
def main():
    load_styles()
    sidebar()
    main_ui()

if __name__ == "__main__":
    main()
