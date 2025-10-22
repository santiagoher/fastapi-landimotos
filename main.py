# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import mensajeros
from dotenv import load_dotenv

# Cargar .env en desarrollo
load_dotenv()

app = FastAPI(title="API Mensajeros - Supabase")

# Ajusta allow_origins a tu dominio de producción para mayor seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción: ["https://landimotos.net"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mensajeros.router)

@app.get("/")
def root():
    return {"message": "API conectada con Supabase mensajeros"}
