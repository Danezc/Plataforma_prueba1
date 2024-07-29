import requests
import config  # Archivo de configuración con la URL de la API

def authenticate_user(username, password):
    # Lógica para conectarse a la API y verificar las credenciales
    response = requests.post(
        f"{config.API_URL}/auth/login",
        json={"username": username, "password": password},
    )
    if response.status_code == 200:
        return True
    else:
        return False
