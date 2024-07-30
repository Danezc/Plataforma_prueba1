import streamlit as st
import bcrypt
import sqlite3

from utils.permissions import get_modulos_permitidos

def authenticate_user(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol_id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row is not None:
            hashed_password, rol = row

            # Verificar si la contraseña ya está hasheada
            if hashed_password.startswith(b"$2b$") or hashed_password.startswith(b"$2y$"):
                if bcrypt.checkpw(password.encode(), hashed_password):  # Ya está hasheada, verificar directamente
                    modulos_permitidos = get_modulos_permitidos(rol)
                    return {"rol_id": rol, "modulos": modulos_permitidos}
            else:  # Contraseña no hasheada
                new_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                
                # Actualizar la contraseña en la base de datos
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed_password, username))
                conn.commit()

                modulos_permitidos = get_modulos_permitidos(rol)
                return {"rol_id": rol, "modulos": modulos_permitidos}  # Retornamos los datos después de hashear

    return None  # Retornamos None si la autenticación falla

