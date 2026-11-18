from collections.abc import Sequence
from datetime import date, timedelta

from fastapi import HTTPException

from dependencies import (
    LibroRepositoryDep,
    PrestamoRepositoryDep,
    SocioRepositoryDep,
)
from models.prestamos import Prestamo, PrestamoBase

MAX_PRESTAMOS_ACTIVOS = 3
DIAS_DE_PRESTAMO = 14
MULTA_POR_DIA = 100


class PrestamoService:
    def __init__(
        self,
        repo: PrestamoRepositoryDep,
        libro_repo: LibroRepositoryDep,
        socio_repo: SocioRepositoryDep,
    ):
        self.repo = repo
        self.libro_repo = libro_repo
        self.socio_repo = socio_repo

    def listar(self) -> Sequence[Prestamo]:
        return self.repo.listar()

    def obtener(self, prestamo_id: int) -> Prestamo | None:
        return self.repo.obtener(prestamo_id)

    def listar_por_socio(
        self, socio_id: int, activos: bool | None = None
    ) -> Sequence[Prestamo]:
        if self.socio_repo.obtener(socio_id) is None:
            raise HTTPException(status_code=404, detail="Socio no encontrado")
        return self.repo.listar_por_socio(socio_id, activos)

    def prestar(self, datos: PrestamoBase) -> Prestamo:
        socio = self.socio_repo.obtener(datos.socio_id)
        if socio is None:
            raise HTTPException(status_code=404, detail="Socio no encontrado")

        libro = self.libro_repo.obtener(datos.libro_id)
        if libro is None:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        if not socio.activo:
            raise HTTPException(
                status_code=403, detail="El socio está inactivo"
            )

        activos = self.repo.listar_por_socio(datos.socio_id, activos=True)
        if len(activos) >= MAX_PRESTAMOS_ACTIVOS:
            raise HTTPException(
                status_code=409,
                detail="El socio ya tiene 3 préstamos activos",
            )

        if libro.stock == 0:
            raise HTTPException(
                status_code=409, detail="El libro no tiene stock"
            )

        hoy = date.today()
        prestamo = Prestamo(
            socio_id=datos.socio_id,
            libro_id=datos.libro_id,
            fecha_prestamo=hoy,
            fecha_vencimiento=hoy + timedelta(days=DIAS_DE_PRESTAMO),
        )
        libro.stock -= 1
        return self.repo.guardar(prestamo, libro)

    def devolver(self, prestamo_id: int) -> Prestamo:
        prestamo = self.repo.obtener(prestamo_id)
        if prestamo is None:
            raise HTTPException(
                status_code=404, detail="Préstamo no encontrado"
            )

        if prestamo.fecha_devolucion is not None:
            raise HTTPException(
                status_code=409, detail="El préstamo ya fue devuelto"
            )

        libro = self.libro_repo.obtener(prestamo.libro_id)
        if libro is None:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        hoy = date.today()
        dias_de_atraso = (hoy - prestamo.fecha_vencimiento).days
        prestamo.fecha_devolucion = hoy
        prestamo.multa = max(dias_de_atraso, 0) * MULTA_POR_DIA
        libro.stock += 1
        return self.repo.guardar(prestamo, libro)