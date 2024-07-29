import streamlit as st
from PIL import Image

def show_logo():
    logo_path = "assets/images/LOGYCA_logo.png"
    logo = Image.open(logo_path)
    st.image(logo, use_column_width=True)
    # Añadir el texto debajo de la imagen (con la clase CSS)
    st.markdown(
        """
        <div style="text-align: center;">
            <p class="logo-caption">Plataforma de operaciones LOGYCA / ANALITICA</p>
        </div>
        """,
        unsafe_allow_html=True,
    )