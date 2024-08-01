from utils.permissions import get_modulos_permitidos

import sqlite3
import bcrypt

def authenticate_user(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        # Consulta para obtener el rol directamente en el JOIN
        cursor.execute("""
            SELECT users.password, users.rol_id, users.nombre, roles.rol 
            FROM users 
            JOIN roles ON users.rol_id = roles.id
            WHERE username = ?
        """, (username,))
        row = cursor.fetchone()

        if row is not None:
            stored_password, rol_id, nombre, rol = row  # Obtener el rol directamente
            password_bytes = password.encode()

            # Verificar si coincide en texto plano (contraseñas no hasheadas)
            if password == stored_password:
                # Hashear la contraseña y actualizar en la base de datos
                new_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed_password, username))
                conn.commit()

                modulos_permitidos = get_modulos_permitidos(rol_id)
                return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre, "rol": rol}  # Incluir el rol

            # Verificar si la contraseña almacenada es un hash bcrypt válido
            try:
                if bcrypt.checkpw(password_bytes, stored_password):
                    modulos_permitidos = get_modulos_permitidos(rol_id)
                    return {"rol_id": rol_id, "modulos": modulos_permitidos, "nombre": nombre, "rol": rol}  # Incluir el rol
            except ValueError:
                print('La contraseña almacenada no es un hash bcrypt válido.')
                pass  # La contraseña almacenada no es un hash bcrypt válido

    return None  # Usuario no encontrado o contraseña incorrecta





