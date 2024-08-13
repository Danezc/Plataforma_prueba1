import streamlit as st
import sqlite3
import bcrypt

from utils import sidebar


def app():

    """
    Función para cambiar la contraseña de un usuario autenticado.

    Esta función permite a un usuario cambiar su contraseña actual por una nueva.
    Verifica la contraseña actual, valida la nueva contraseña y la actualiza en la base de datos.

    Pasos:

    1. **Obtener el nombre de usuario:** Obtiene el nombre de usuario del usuario autenticado
       almacenado en la sesión de Streamlit.
    2. **Mostrar formulario:** Presenta un formulario con campos para ingresar la contraseña actual,
       la nueva contraseña y la confirmación de la nueva contraseña.
    3. **Validar contraseña actual:** Verifica si la contraseña actual ingresada coincide con la
       contraseña almacenada en la base de datos.
    4. **Validar nueva contraseña:** Verifica si la nueva contraseña cumple con los requisitos de
       seguridad (al menos 8 caracteres, una minúscula, una mayúscula y un número).
    5. **Validar confirmación:** Verifica si la nueva contraseña y la confirmación coinciden.
    6. **Actualizar contraseña:** Si todas las validaciones son exitosas, actualiza la contraseña
       en la base de datos utilizando bcrypt.hashpw para generar un nuevo hash de la contraseña.
    7. **Mostrar mensajes:** Muestra mensajes de éxito o error al usuario según el resultado de
       la operación.

    Returns:
        bool: True si la contraseña se cambió correctamente, False en caso contrario.
    """
    
    st.subheader("Cambiar Contraseña")
    sidebar.sidebar("cambiar_contrasena")

    # Obtener el nombre de usuario de la sesión
    username = st.session_state.get("username")

    if not username:
        st.error("No hay ningún usuario autenticado.")
        return False

    with st.form("change_password_form"):
        # Campos para ingresar contraseñas
        contrasena_actual = st.text_input("Contraseña Actual", type="password")
        contrasena_nueva = st.text_input("Contraseña Nueva", type="password")
        repetir_contrasena = st.text_input("Repetir Contraseña Nueva", type="password")

        if st.form_submit_button("Cambiar Contraseña"):
            # Verificar contraseña actual (usando bcrypt.checkpw)
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            resultado = cursor.fetchone()

            if resultado:
                contrasena_hash_db = resultado[0]
                
                # Verificar si la contraseña actual coincide con el hash en la base de datos
                if bcrypt.checkpw(contrasena_actual.encode(), contrasena_hash_db):
                    # verificar que contrasena_nueva tenga minusculas, mayusculas, numeros y al menos 8 caracteres
                    if not any(char.islower() for char in contrasena_nueva) or not any(char.isupper() for char in contrasena_nueva) or not any(char.isdigit() for char in contrasena_nueva) or len(contrasena_nueva) < 8:
                        st.error("La contraeseña debe tener al menos 8 cáracteres, una minuscula, una mayuscula y un numero")
                        return False
                    
                    if contrasena_nueva != repetir_contrasena:
                        st.error("Las contraseñas nuevas indicadas no coinciden.")
                        return False

                    # Actualizar contraseña si todo es válido (usando bcrypt.hashpw)
                    nueva_contrasena_hash = bcrypt.hashpw(contrasena_nueva.encode(), bcrypt.gensalt())
                    cursor.execute("UPDATE users SET password = ? WHERE username = ?",
                                   (nueva_contrasena_hash, username))
                    conn.commit()
                    conn.close()
                    st.success("Contraseña cambiada con éxito.")
                    return True

                else:
                    st.error("La contraseña actual es incorrecta.")
                    return False
            else:
                st.error("Usuario no encontrado.")
                return False

    return False  # No se realizaron cambios
