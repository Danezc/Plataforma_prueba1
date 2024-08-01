import streamlit as st
from utils import  sidebar
import asyncio
import threading

from Alarmas.ejecutar_codigo import ejecutar_codigo_async


def app():
    if "user_data" in st.session_state:
        sidebar.sidebar("Alarmas")
        st.markdown('<div style="margin-top: 15vh;">', unsafe_allow_html=True)

        st.markdown("## Creador de Alarmas LOGYCA V18.2")

        # Subir archivo Excel
        uploaded_file = st.file_uploader("Seleccionar consolidado", type=["xlsx"])

        if uploaded_file is not None:
            # Ejecutar el código en un hilo separado
            if st.button("Ejecutar código"):
                with st.spinner("Procesando..."):
                    def ejecutar_en_hilo():
                        # Crear un bucle de eventos temporal
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                        # Ejecutar la función async en el bucle
                        loop.run_until_complete(ejecutar_codigo_async(uploaded_file))

                    hilo = threading.Thread(target=ejecutar_en_hilo)
                    hilo.start()
                    hilo.join()  # Esperar a que el hilo termine

                    st.success("Proceso completado.")

    else:
        st.warning("No has iniciado sesión.")
