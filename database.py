# database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar .env en desarrollo (Render/producción usan variables de entorno del entorno)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en las variables de entorno.")

# Crear cliente Supabase (sincrono)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)