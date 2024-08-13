import hashlib
import os
import streamlit as st
from PIL import Image
from utils.normalice import normalize_module_name


def generar_clave_unica(nombre_pagina, contexto):
    """Genera una clave única basada en el nombre de la página y un contexto adicional."""
    return nombre_pagina + "_" + hashlib.md5((nombre_pagina + contexto).encode()).hexdigest()[:8]

def mostrar_logo():
    """Muestra el logo de LOGYCA en la barra lateral."""

    logo_path = "assets/images/LOGYCA_logo.png"
    with Image.open(logo_path) as logo:
        logo = logo.resize((330, 100))
        st.sidebar.image(logo)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

def gestionar_boton_pagina(pagina, contexto):
    page_name_normalized = normalize_module_name(pagina)
    page_path = os.path.join("pages", page_name_normalized + ".py")

    if os.path.exists(page_path):
        clave_unica = generar_clave_unica(page_name_normalized, contexto)  

        current_page = st.session_state.get("current_page", None)
        is_current_page = current_page == page_name_normalized

        with st.sidebar: 
            if st.button(pagina, key=clave_unica, disabled=is_current_page):
                try:
                    module = __import__(f"pages.{page_name_normalized}", fromlist=[""])
                    app_function = getattr(module, "app", None)
                    if app_function:
                        app_function()
                        st.session_state["current_page"] = page_name_normalized
                        st.rerun()  
                    else:
                        st.error(f"No se encontró la función 'app' en la página '{pagina}'.")
                except ModuleNotFoundError:
                    st.error(f"Error al importar la página '{pagina}'.")
    else:
        st.warning(f"La página '{pagina}' no fue encontrada en la carpeta 'pages'.")

def gestionar_botones_paginas(contexto):
    if "user_data" in st.session_state:
        for pagina in st.session_state["user_data"]["modulos"]:
            gestionar_boton_pagina(pagina, contexto)

def logout_button():
    """
    Muestra el botón de cierre de sesión en la barra lateral.

    Aplica estilos CSS para un aspecto consistente con otros botones.
    """
    button_style = f"""
        display: block; 
        width: 100%;   
        background-color: inherit;
        color: inherit;
        pointer-events: auto;
        cursor: pointer;
        border: none;
        border-bottom: 1px solid #ddd; 
        padding: 0px 0;  
        text-align: center;
        text-decoration: none;
        font-size: 22px;  
        margin-bottom: 0.15%; 
    """

    with st.sidebar: 
        # Se aplica el estilo al botón
        st.markdown(
            f'<style>button[data-baseweb="button"] {{ {button_style} }}</style>',
            unsafe_allow_html=True,
        )
        if st.button("Cerrar sesión", key="logout_button"):  # Clave única para el botón
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state["authenticated"] = False
            st.session_state["current_page"] = "login"
            st.rerun()

def ocultar_navegacion_sidebar():
    hide_sidebar_nav = """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
    """
    st.markdown(hide_sidebar_nav, unsafe_allow_html=True)

def sidebar(contexto):
    mostrar_logo()
    gestionar_botones_paginas(contexto)
    logout_button()
    ocultar_navegacion_sidebar()
