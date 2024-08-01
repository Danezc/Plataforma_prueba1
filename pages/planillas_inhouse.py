import streamlit as st
from utils import  sidebar


def app():
    if "user_data" in st.session_state:
        sidebar.sidebar("Plantillas_inhouse")
        st.markdown('<div style="margin-top: 15vh;">', unsafe_allow_html=True)
        st.title(f"Bienvenido a planillas ih, {st.session_state['user_data']['nombre']}")


        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No has iniciado sesión.")
