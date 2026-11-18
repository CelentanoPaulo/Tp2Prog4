from fastapi import APIRouter, HTTPException

from dependencies import SocioServiceDep
from models.socios import SocioBase, SocioPublic

router = APIRouter(prefix="/socios", tags=["Socios"])


@router.get("", response_model=list[SocioPublic])
def listar_socios(service: SocioServiceDep):
    return service.listar()


@router.get("/{socio_id}", response_model=SocioPublic)
def obtener_socio(socio_id: int, service: SocioServiceDep):
    socio = service.obtener(socio_id)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio


@router.post("", response_model=SocioPublic, status_code=201)
def crear_socio(datos: SocioBase, service: SocioServiceDep):
    return service.crear(datos)


@router.put("/{socio_id}", response_model=SocioPublic)
def actualizar_socio(
    socio_id: int, datos: SocioBase, service: SocioServiceDep
):
    socio = service.actualizar(socio_id, datos)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio


@router.delete("/{socio_id}", status_code=204)
def eliminar_socio(socio_id: int, service: SocioServiceDep):
    if not service.eliminar(socio_id):
        raise HTTPException(status_code=404, detail="Socio no encontrado")