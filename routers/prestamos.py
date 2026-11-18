from fastapi import APIRouter, HTTPException

from dependencies import PrestamoServiceDep
from models.prestamos import PrestamoBase, PrestamoPublic

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.get("", response_model=list[PrestamoPublic])
def listar_prestamos(service: PrestamoServiceDep):
    return service.listar()


@router.get("/{prestamo_id}", response_model=PrestamoPublic)
def obtener_prestamo(prestamo_id: int, service: PrestamoServiceDep):
    prestamo = service.obtener(prestamo_id)
    if prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


@router.post("", response_model=PrestamoPublic, status_code=201)
def registrar_prestamo(datos: PrestamoBase, service: PrestamoServiceDep):
    return service.prestar(datos)


@router.post("/{prestamo_id}/devolucion", response_model=PrestamoPublic)
def registrar_devolucion(prestamo_id: int, service: PrestamoServiceDep):
    return service.devolver(prestamo_id)