import streamlit as st
from utils import auth, ui
import config

def app():
    # Mostrar el logo
    ui.show_logo()

    # Formulario de inicio de sesión
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit_button = st.form_submit_button("Iniciar Sesión")

    # Lógica de verificación de credenciales
    if submit_button:
        user_data = auth.authenticate_user(username, password)
        if user_data:
            st.session_state["user_data"] = user_data
            st.session_state["authenticated"] = True  # Marcamos como autenticado
            st.session_state["current_page"] = "panel_ingreso"  # Redirección directa
            st.rerun()  # Recargamos la página para aplicar los cambios
        else:
            st.error("Credenciales incorrectas")
