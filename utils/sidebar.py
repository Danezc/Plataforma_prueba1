import streamlit as st
from PIL import Image
from utils.normalice import normalize_module_name
import os




def logout_button():
    if st.button("Cerrar sesión"):
        # Borrar datos de la sesión
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["authenticated"] = False

        # Redirigir a la página de inicio de sesión (login.py)
        st.session_state["current_page"] = "login"
        st.rerun()  # Recargar la aplicación para aplicar los cambios

def sidebar():
    logo_path = "assets/images/LOGYCA_logo.png"

    st.markdown(
        f'<link rel="stylesheet" href="styles.css">',
        unsafe_allow_html=True,
    )

    with Image.open(logo_path) as logo:
        logo = logo.resize((300, 100))

    st.sidebar.image(logo)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

    if "user_data" in st.session_state:
        for pagina in st.session_state["user_data"]["modulos"]:
            # Normalizar el nombre de la página para que coincida con el archivo
            page_name = normalize_module_name(pagina) + ".py" 

            # Construir la ruta completa al archivo de la página
            page_path = os.path.join("pages", page_name)

            if os.path.exists(page_path):  # Verificar si el archivo existe
                if st.sidebar.button(pagina):  # Simplificar el condicional del botón
                    try:
                        module = __import__(f"pages.{normalize_module_name(pagina)}", fromlist=[""])
                        app_function = getattr(module, "app", None)  # Obtener la función app si existe

                        if app_function:
                            app_function()
                            st.session_state["current_page"] = normalize_module_name(pagina)
                            st.rerun()
                        else:
                            st.error(f"No se encontró la función 'app' en la página '{pagina}'.")
                    except ModuleNotFoundError:
                        st.error(f"Error al importar la página '{pagina}'.")
            else:
                st.warning(f"La página '{pagina}' no fue encontrada en la carpeta 'pages'.")


    st.markdown("</div>", unsafe_allow_html=True)
    logout_button()

    # Ocultar la navegación del sidebar
    hide_sidebar_nav = """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
    """
    st.markdown(hide_sidebar_nav, unsafe_allow_html=True)

