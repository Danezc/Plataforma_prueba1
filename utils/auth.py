import streamlit as st
import bcrypt
import pyodbc

# Configuración de la conexión a Azure SQL
CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server_name.database.windows.net;DATABASE=your_database_name;UID=your_username;PWD=your_password"

def authenticate_user(username, password):
    with pyodbc.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password, rol FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

            if row and bcrypt.checkpw(password.encode(), row[0].encode()):
                st.session_state["rol"] = row[1]  # Almacenar el rol en la sesión
                return True
    return False