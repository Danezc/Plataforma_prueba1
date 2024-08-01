import sqlite3

def get_modulos_permitidos(user_id):
    # Recibe el ID del usuario, no el rol
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT modulos.nombre  -- Seleccionamos el nombre del módulo
            FROM roles_modulos_usuarios
            JOIN modulos ON roles_modulos_usuarios.modulo_id = modulos.id
            JOIN users ON roles_modulos_usuarios.rol_id = users.rol_id  -- Unimos con la tabla users
            WHERE users.id = ?  -- Filtramos por el ID del usuario
        ''', (user_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]  # Devolvemos una lista de nombres de módulos