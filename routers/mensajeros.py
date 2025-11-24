# routers/mensajeros.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from starlette.concurrency import run_in_threadpool
from database import supabase

router = APIRouter(prefix="/mensajeros", tags=["Mensajeros"])

# Modelo Pydantic
class ActualizarEntrega(BaseModel):
    estado: str
    hora_llegada: Optional[str] = None


@router.put("/actualizarRegistro/{id_registro}")
async def actualizar_registro(id_registro: int, datos: ActualizarEntrega):
    try:
        # 1. Verificar si el registro existe
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

        # 2. Preparar campos a actualizar
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
