import streamlit as st
from utils import  sidebar
import streamlit as st
import contextlib
import io

from Disponible_sistemico.ejecutar_codigo import ejecutar_codigo


def app():

    sidebar.sidebar("Disponible Sistémico")

    st.title('Disponible Sistémico LOGYCA V.1.0')

    # Entradas de archivos
    entradas_path = {}
    for nombre_archivo in ["Cronograma", "Vectorización", "Datos de DDVI"]:
        uploaded_file = st.file_uploader(f"Seleccionar {nombre_archivo}", type=["xlsx"])
        entradas_path[nombre_archivo] = uploaded_file

    # Botón Ejecutar
    if st.button("Ejecutar código"):
        if all(entradas_path.values()): 
            with st.spinner("Procesando..."):
                # Redirigir la salida estándar a un área de texto en Streamlit
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    # Ejecutar el código
                    ejecutar_codigo(entradas_path)

                # Mostrar la salida en el área de texto
                st.text_area("Consola", value=output.getvalue(), height=200)

                st.success("Ejecución finalizada")
        else:
            st.warning("Por favor, selecciona todos los archivos necesarios.")

