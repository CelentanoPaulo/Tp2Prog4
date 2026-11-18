from fastapi import APIRouter, HTTPException

from dependencies import AutorServiceDep
from models.libros import AutorBase, AutorPublic

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("", response_model=list[AutorPublic])
def listar_autores(service: AutorServiceDep):
    return service.listar()


@router.get("/{autor_id}", response_model=AutorPublic)
def obtener_autor(autor_id: int, service: AutorServiceDep):
    autor = service.obtener(autor_id)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@router.post("", response_model=AutorPublic, status_code=201)
def crear_autor(datos: AutorBase, service: AutorServiceDep):
    return service.crear(datos)


@router.put("/{autor_id}", response_model=AutorPublic)
def actualizar_autor(
    autor_id: int, datos: AutorBase, service: AutorServiceDep
):
    autor = service.actualizar(autor_id, datos)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@router.delete("/{autor_id}", status_code=204)
def eliminar_autor(autor_id: int, service: AutorServiceDep):
    if not service.eliminar(autor_id):
        raise HTTPException(status_code=404, detail="Autor no encontrado")