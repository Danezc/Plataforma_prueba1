import streamlit as st
from utils import  sidebar


def app():
    if "user_data" in st.session_state:
        # Llamada a la función para ocultar la barra lateral
        sidebar.sidebar()
        st.markdown('<div style="margin-top: 15vh;">', unsafe_allow_html=True)
        st.title(f"Bienvenido, {st.session_state['user_data']['nombre']}")


        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No has iniciado sesión.")
