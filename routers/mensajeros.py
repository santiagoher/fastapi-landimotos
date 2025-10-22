# routers/mensajeros.py
from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool
from database import supabase

router = APIRouter(prefix="/mensajeros", tags=["Mensajeros"])

@router.get("/mostrarRegistro")
async def listar_mensajeros():
    try:
        # Ejecutar la llamada a supabase en un hilo para no bloquear el event loop
        def _call():
            return supabase.table("mensajeros").select("*").execute()
        response = await run_in_threadpool(_call)

        # Si la librería devuelve .data o response.get("data") adaptamos:
        data = getattr(response, "data", None) or (response.get("data") if isinstance(response, dict) else None)
        if data is None:
            # Intenta con response.data si es objeto
            try:
                data = response.data
            except Exception:
                data = []

        return {"total": len(data), "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {e}")

@router.post("/crearRegistro")
async def crear_mensajero(request: Request):
    try:
        data = await request.json()
        # Convertir None -> "" para evitar errores si lo deseas
        data = {k: ("" if v is None else v) for k, v in data.items()}

        def _insert():
            return supabase.table("mensajeros").insert(data).execute()
        response = await run_in_threadpool(_insert)

        inserted = getattr(response, "data", None) or (response.get("data") if isinstance(response, dict) else None)
        if not inserted:
            raise HTTPException(status_code=400, detail="No se pudo insertar el registro")

        return {"message": "Mensajero creado correctamente", "data": inserted}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el registro: {e}")
