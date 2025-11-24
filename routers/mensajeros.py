# routers/mensajeros.py
from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Optional
from database import supabase

router = APIRouter(prefix="/mensajeros", tags=["Mensajeros"])

# Modelo Pydantic
class ActualizarEntrega(BaseModel):
    estado: str
    hora_llegada: Optional[str] = None


@router.get("/mostrarRegistro")
async def listar_mensajeros():
    try:
        def _call():
            return supabase.table("mensajeros").select("*").execute()

        response = await run_in_threadpool(_call)

        data = getattr(response, "data", None) or (
            response.get("data") if isinstance(response, dict) else None
        )
        if data is None:
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
        data = {k: ("" if v is None else v) for k, v in data.items()}

        def _insert():
            return supabase.table("mensajeros").insert(data).execute()

        response = await run_in_threadpool(_insert)

        inserted = getattr(response, "data", None) or (
            response.get("data") if isinstance(response, dict) else None
        )

        if not inserted:
            raise HTTPException(status_code=400, detail="No se pudo insertar el registro")

        return {"message": "Mensajero creado correctamente", "data": inserted}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el registro: {e}")


@router.put("/actualizarRegistro/{id_registro}")
async def actualizar_registro(id_registro: int, datos: ActualizarEntrega):
    try:
        # 1. Buscar registro
        def _buscar():
            return (
                supabase.table("mensajeros")
                .select("*")
                .eq("id", id_registro)
                .execute()
            )

        resultado = await run_in_threadpool(_buscar)
        registro = getattr(resultado, "data", None)

        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        # 2. Armar los campos a actualizar
        update_data = {"estado": datos.estado}

        if datos.hora_llegada:
            update_data["hora_llegada"] = datos.hora_llegada

        # 3. Ejecutar actualización
        def _actualizar():
            return (
                supabase.table("mensajeros")
                .update(update_data)
                .eq("id", id_registro)
                .execute()
            )

        response_update = await run_in_threadpool(_actualizar)
        updated = getattr(response_update, "data", None)

        return {"mensaje": "Registro actualizado correctamente", "data": updated}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar el registro: {e}"
        )
