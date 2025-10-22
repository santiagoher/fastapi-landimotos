from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import mensajeros
from fastapi.responses import JSONResponse


app = FastAPI(title="API Mensajeros - Supabase")

# 🔒 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Incluir router principal
app.include_router(mensajeros.router)   

@app.get("/")
def root():
    return {"message": "API conectada con Supabase mensajeros"}

