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

            # Verificar si coincide en texto plano (contraseñas no hasheadas)
            if password == stored_password:
                # Hashear la contraseña y actualizar en la base de datos
                new_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed_password, username))
                conn.commit()

                modulos_permitidos = get_modulos_permitidos(rol_id)
                return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre}

            # Verificar si la contraseña almacenada es un hash bcrypt válido
            try:
                if bcrypt.checkpw(password_bytes, stored_password):
                    modulos_permitidos = get_modulos_permitidos(rol_id)
                    return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre}
            except ValueError:
                print('La contraseña almacenada no es un hash bcrypt válido.')
                pass  # La contraseña almacenada no es un hash bcrypt válido

    return None  # Usuario no encontrado o contraseña incorrecta




