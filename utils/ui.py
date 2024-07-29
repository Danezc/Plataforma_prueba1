import streamlit as st
from PIL import Image

def show_logo():
    logo_path = "assets/images/LOGYCA_logo.png"
    logo = Image.open(logo_path)
    st.image(logo, use_column_width=True)
