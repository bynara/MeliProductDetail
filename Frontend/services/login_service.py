import requests

# Configuration
auth_url = "http://localhost:8000/token"
products_url = "http://localhost:8000/sellers"

# Obtener token
def get_token(username: str, password: str) -> str:
    auth_response = requests.post(auth_url, data={
        "grant_type": "password",
        "username": username,
        "password": password
    })
    auth_response.raise_for_status()
    return auth_response.json()["access_token"]
