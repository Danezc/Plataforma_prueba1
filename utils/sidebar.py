import hashlib
import os
import streamlit as st
from PIL import Image
from utils.normalice import normalize_module_name


def generar_clave_unica(nombre_pagina, contexto):
    """Genera una clave única basada en el nombre de la página y un contexto adicional."""
    return nombre_pagina + "_" + hashlib.md5((nombre_pagina + contexto).encode()).hexdigest()[:8]

def mostrar_logo():
    logo_path = "assets/images/LOGYCA_logo.png"
    with Image.open(logo_path) as logo:
        logo = logo.resize((300, 100))
        st.sidebar.image(logo)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

def gestionar_boton_pagina(pagina, contexto):
    page_name_normalized = normalize_module_name(pagina)
    page_path = os.path.join("pages", page_name_normalized + ".py")

    if os.path.exists(page_path):
        clave_unica = generar_clave_unica(page_name_normalized, contexto)  # Pasa el nombre normalizado y el contexto
        if st.sidebar.button(pagina, key=clave_unica):
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
    if st.sidebar.button("Cerrar sesión", key="logout_button"):  # Clave única para el botón
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
    st.markdown(
        f'<link rel="stylesheet" href="styles.css">',
        unsafe_allow_html=True,
    )
    mostrar_logo()
    gestionar_botones_paginas(contexto)
    logout_button()
    ocultar_navegacion_sidebar()


