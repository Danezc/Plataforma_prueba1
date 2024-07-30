from utils.permissions import get_modulos_permitidos

import sqlite3
import bcrypt

def authenticate_user(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol_id, nombre FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row is not None:
            stored_password, rol_id, nombre = row 
            password_bytes = password.encode()

            try:  
                if bcrypt.checkpw(password_bytes, stored_password):  # Quita .encode() aquí
                    modulos_permitidos = get_modulos_permitidos(rol_id)
                    return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre}
            except ValueError:  
                new_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                # Actualizar la contraseña en la base de datos (opcional, pero recomendado)
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed_password, username))
                conn.commit()
                # Ahora, intenta verificar de nuevo
                if bcrypt.checkpw(password.encode(), new_hashed_password):
                    modulos_permitidos = get_modulos_permitidos(rol_id)
                    return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre}
        return None  # Usuario no encontrado o contraseña incorrecta




