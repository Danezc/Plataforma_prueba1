import streamlit as st
from PIL import Image
import inspect  # Para inspeccionar funciones


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

    # Mostrar las páginas permitidas como botones
    if "user_data" in st.session_state:
        for pagina in st.session_state["user_data"]["modulos"]:
            if st.sidebar.button(pagina):
                try:
                    # Importación dinámica de la página
                    page_name = pagina.lower().replace(" ", "_")
                    module = __import__(f"pages.{page_name}", fromlist=[""])

                    # Buscar la función app dentro de la página
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj) and name == "app":
                            obj()  # Ejecutar la función app
                            break
                    else:
                        st.error(f"No se encontró la función 'app' en la página '{pagina}'.")

                except ModuleNotFoundError:
                    st.error(f"La página '{pagina}' no fue encontrada.")

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
