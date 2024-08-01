import streamlit as st
from utils import sidebar

import streamlit as st
import json


def app():
    if "user_data" in st.session_state:
        sidebar.sidebar("Panel de ingreso")
        st.markdown('<div style="margin-top: 15vh;">', unsafe_allow_html=True)
        st.title(f"Bienvenido, {st.session_state['user_data']['nombre']} al modulo de operaciones de {st.session_state['user_data']['rol']}")

        # Tablero de anuncios
        st.subheader("Tablero de Anuncios")

        try:
            with open("mensajes.json", "r") as f:
                mensajes = json.load(f)
        except FileNotFoundError:
            mensajes = []

        # Mostrar los últimos 3 mensajes
        for mensaje in mensajes[-3:]:
            st.write(f"**{mensaje['usuario']}:** {mensaje['texto']}")

        # Formulario para agregar un nuevo mensaje
        with st.form("nuevo_mensaje"):
            nuevo_mensaje = st.text_area("Escribe tu mensaje:")
            if st.form_submit_button("Publicar"):
                mensajes.append({"usuario": st.session_state['user_data']['nombre'], "texto": nuevo_mensaje})
                with open("mensajes.json", "w") as f:
                    json.dump(mensajes, f)
                st.rerun()  # Recargar la página para mostrar el nuevo mensaje

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No has iniciado sesión.")
