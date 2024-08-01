import streamlit as st
from pages.login import login_app
import re

# Configuración de la página
st.set_page_config(
    page_title="LOGYCA / OPERACIONES ANALITICA",
    page_icon="assets/images/favicon.ico",
    layout="wide",
)

# Función de navegación
def navigate_to(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

# Función para convertir el nombre del módulo a un nombre de archivo válido
def normalize_module_name(module_name):
    # Convertir a minúsculas
    module_name = module_name.lower()
    # Eliminar tildes y caracteres especiales
    module_name = re.sub(r'[^\w\s]', '', module_name)
    # Reemplazar espacios por guiones bajos
    module_name = module_name.replace(' ', '_')
    return module_name

# Control de navegación
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login_app()  # Mostrar página de login si no está autenticado
else:
    # Inicializar estado de la sesión
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "panel_ingreso"

    # Obtener la página actual
    current_page = st.session_state["current_page"]

    print(f"current_page: {current_page}")
    
    # Verificar si el usuario tiene acceso al módulo actual
    user_data = st.session_state.get("user_data", {})
    modulos_permitidos = user_data.get("modulos", [])

    print(f"modulos_permitidos: {modulos_permitidos}")

    # Normalizar el nombre del módulo actual
    normalized_current_page = normalize_module_name(current_page)

    # Verificar si el módulo normalizado está en la lista de módulos permitidos
    if normalized_current_page in [normalize_module_name(m) for m in modulos_permitidos]:
        # Importación dinámica del módulo
        try:
            page = __import__(f"pages.{normalized_current_page}", fromlist=[""])
            print(f"Buscando la página en: pages/{normalized_current_page}")  # Imprime la ruta
        except ImportError as e:
            st.error(f"Error al cargar el módulo '{current_page}': {e}")
            st.session_state["current_page"] = "panel_ingreso"
            st.rerun()

        # Mostrar la página correspondiente
        with st.container():
            page.app()
    else:
        # Redirigir a una página permitida (por ejemplo, "panel_ingreso")
        st.error("No tienes acceso a esta página.")
        st.session_state["current_page"] = "panel_ingreso"  # Redirige a una página permitida
        st.rerun()
