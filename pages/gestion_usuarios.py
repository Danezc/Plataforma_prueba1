import streamlit as st
import pandas as pd
import sqlite3


def app():
    st.title("Gestión de Usuarios")

    # Conexión a la base de datos (ajusta la ruta si es necesario)
    conn = sqlite3.connect('users.db')  
    cursor = conn.cursor()

    # Obtener roles disponibles
    roles_df = pd.read_sql_query("SELECT id, rol FROM roles", conn)
    roles_dict = roles_df.set_index('id')['rol'].to_dict()

    # Mostrar tabla de usuarios con el rol
    df_users = pd.read_sql_query("SELECT username, nombre, roles.rol, activo FROM users JOIN roles ON users.rol_id = roles.id", conn)
    df_users['activo'] = df_users['activo'].astype(bool)
    edited_df = st.data_editor(df_users, num_rows="dynamic")
    cambios_realizados = False

    # Guardar cambios en la tabla (solo para la columna 'activo')
    for index, row in edited_df.iterrows():
        cursor.execute(
            "UPDATE users SET activo = ? WHERE username = ?",
            (int(row['activo']), row['username'])
        )
    conn.commit()
    cambios_realizados = True  # Marcar cambios


    # Agregar nuevo usuario con selección de rol
    with st.form("add_user_form"):
        st.subheader("Agregar Nuevo Usuario")
        new_username = st.text_input("Nombre de Usuario", key="new_username")
        new_nombre = st.text_input("Nombre Completo", key="new_nombre")
        selected_rol_id = st.selectbox("Rol", options=list(roles_dict.keys()), format_func=lambda x: roles_dict[x])
        if st.form_submit_button("Agregar Usuario"):
            if new_username and new_nombre:
                try:
                    cursor.execute(
                        "INSERT INTO users (username, nombre, password, rol_id) VALUES (?, ?, ?, ?)",
                        (new_username, new_nombre, "Logyca2023*", selected_rol_id)
                    )
                    conn.commit()
                    cambios_realizados = True

                    st.success(f"Usuario '{new_username}' agregado con éxito.")
                    # Update the UI directly
                    df_users = pd.read_sql_query("SELECT username, nombre, roles.rol, activo FROM users JOIN roles ON users.rol_id = roles.id", conn)
                    df_users['activo'] = df_users['activo'].astype(bool)
                    edited_df = st.data_editor(df_users, num_rows="dynamic")

                    # Clear the form fields
                    st.session_state.new_username = ""
                    st.session_state.new_nombre = ""

                except sqlite3.IntegrityError:
                    st.error("El nombre de usuario ya existe.")

    
    conn.close()
    return cambios_realizados

