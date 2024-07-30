import streamlit as st
from PIL import Image

def show_logo():
    logo_path = "assets/images/LOGYCA_logo.png"  # Asegúrate de que la ruta sea correcta
    
    # Cargar y redimensionar el logo
    with Image.open(logo_path) as logo:
        logo = logo.resize((1500, 400))  # Ajusta el tamaño segúns tus preferencias
    
    # Mostrar el logo centrado
    col1, col2, col3 = st.columns([1, 2, 1])  # Tres columnas para centrar
    with col2:
        st.image(logo)

    # Aplicar estilos CSS al texto
    st.markdown(
        """
        <style>
        .stCaption {
            font-size: 40px; 
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Mostrar el texto con el estilo aplicado
    st.markdown(
        f"<h1 class='stCaption'>Plataforma de operaciones LOGYCA / ANALITICA</h1>",
        unsafe_allow_html=True
    )
