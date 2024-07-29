import streamlit as st
from utils import auth, ui

# Configuración de colores 
primary_color = st.get_option("theme.primaryColor")
secondary_color = st.get_option("theme.secondaryBackgroundColor")
text_color = st.get_option("theme.textColor")

# Mostrar el logo
ui.show_logo()

# Formulario de inicio de sesión
with st.form("login_form"):
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    submit_button = st.form_submit_button("Iniciar Sesión")

# Lógica de verificación de credenciales (usando la función de auth.py)
if submit_button:
    if auth.authenticate_user(username, password):
        st.success("Inicio de sesión exitoso")
        # Redirigir a la página principal o mostrar los módulos
    else:
        st.error("Usuario o contraseña incorrectos")
