import streamlit as st
from pages import login, panel_ingreso


# Configuración de la página
st.set_page_config(
    page_title="LOGYCA / OPERACIONES ANALITICA",
    page_icon="assets/images/favicon.ico",
    layout="wide",
)

# Control de navegación
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login.app()  # Mostrar página de login si no está autenticado
elif st.session_state["current_page"] == "panel_ingreso":
    panel_ingreso.app()  # Mostrar lista de módulos si está autenticado
elif st.session_state["current_page"] in st.session_state.get("user_data", {}).get("modulos", []):
    module_name = st.session_state["current_page"]
    module = __import__(f"modules.{module_name}", fromlist=[""])
    module.app()  # Mostrar el módulo correspondiente si está autenticado y tiene permiso
