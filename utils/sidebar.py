import streamlit as st
from PIL import Image

def logout_button():
    if st.button("Cerrar sesión"):
        # Borrar datos de la sesión
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["authenticated"] = False

        # Redirigir a la página de inicio de sesión (login.py)
        st.session_state["current_page"] = "login"
        st.rerun()  # Recargar la aplicación para aplicar los cambios

def sidebar():
    logo_path = "assets/images/LOGYCA_logo.png" # Ruta de la imagen

    with Image.open(logo_path) as logo:
        logo = logo.resize((150, 50))

    st.sidebar.image(logo)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)  # Espacio entre logo y botones

    # Mostrar los módulos permitidos como botones
    if "user_data" in st.session_state:
        for modulo in st.session_state["user_data"]["modulos"]:
            if st.sidebar.button(modulo):
                st.session_state["current_page"] = modulo
                st.rerun()

    # Botón de cerrar sesión en la parte inferior
    logout_button()
