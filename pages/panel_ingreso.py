import streamlit as st

def app():
    if "user_data" in st.session_state:
        st.title(f"Bienvenido, {st.session_state['user_data']['rol']}")

        # Mostrar los módulos permitidos como botones
        for modulo in st.session_state["user_data"]["modulos"]:
            if st.button(modulo):
                st.session_state["current_page"] = modulo
                st.rerun()  # Recargar la página para mostrar el módulo seleccionado
    else:
        st.warning("No has iniciado sesión.")
