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

import streamlit as st
from PIL import Image

def logout_button():
    if st.button("Cerrar sesión"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["authenticated"] = False
        st.rerun()

def top_bar():
    logo_path = "assets/images/LOGYCA_logo.png"  # Asegúrate de que la ruta sea correcta

    # Cargar y redimensionar el logo (opcional)
    with Image.open(logo_path) as logo:
        logo = logo.resize((100, 50))  # Ajusta el tamaño según tus preferencias

    st.markdown(
        """
        <style>
        .top-bar {
            background-color: #f0f0f0;
            padding: 10px;
            display: flex;
            align-items: center;  /* Alinear verticalmente al centro */
            height: 15vh; /* 15% de la altura de la ventana */
        }

        .logo-container {
            margin-right: auto; /* Empujar el logo a la izquierda */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="top-bar">', unsafe_allow_html=True)
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo)
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar el contenedor del logo
    logout_button()
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar la barra superior

