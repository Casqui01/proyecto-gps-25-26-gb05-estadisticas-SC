import math
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# --- CONFIGURACIÓN INICIAL ---
url: str = os.getenv("SUPABASE_PROJECT_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
admin_email: str = os.getenv("ADMIN_ESTADISTICAS_CORREO")
admin_pass: str = os.getenv("ADMIN_ESTADISTICAS_PASSWORD")

# Inicializamos el cliente de Supabase
supabase: Client = create_client(url, key)

accessToken: str
refreshToken: str
expiresAt: int


def refresh_token():
    # Hacemos el login
    session = supabase.auth.sign_in_with_password({
        "email": admin_email,
        "password": admin_pass
    })

    # Extraemos el token JWT de la sesión
    accessToken = session.session.access_token
    refreshToken = session.session.refresh_token
    expiresAt = session.session.expires_at

refresh_token()

def get_token():
    if is_token_expiring(): refresh_token()
    return accessToken

def is_token_expiring():
    currentTime = math.floor(datetime.now().timestamp() / 1000)
    timeUntilExpire = expiresAt - currentTime
    return timeUntilExpire < 60
