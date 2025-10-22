from fastapi import APIRouter, HTTPException, Request
# Update the import path if database.py is in another folder, e.g., 'app.database'
# from app.database import supabase

from database import supabase

router = APIRouter(prefix="/mensajeros", tags=["Mensajeros"])

@router.get("/mostrarRegistro")
def listar_mensajeros():
    try:
        response = supabase.table("mensajeros").select("*").execute()
        return {"total": len(response.data), "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {e}")

@router.post("/crearRegistro")
async def crear_mensajero(request: Request):
    try:
        # 🚫 No validamos nada, solo recibimos JSON puro
        data = await request.json()
        print("📦 Datos recibidos:", data)

        # Convertir todos los valores None a string vacío
        data = {k: ("" if v is None else str(v)) for k, v in data.items()}

        # Enviar a Supabase directamente
        response = supabase.table("mensajeros").insert(data).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="No se pudo insertar el registro")

        return {"message": "Mensajero creado correctamente", "data": response.data}

    except Exception as e:
        print("❌ Error al insertar:", e)
        raise HTTPException(status_code=500, detail=f"Error al guardar el registro: {e}")
