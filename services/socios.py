from collections.abc import Sequence

from fastapi import HTTPException

from dependencies import SocioRepositoryDep
from models.socios import Socio, SocioBase


class SocioService:
    def __init__(self, repo: SocioRepositoryDep):
        self.repo = repo

    def listar(self) -> Sequence[Socio]:
        return self.repo.listar()

    def obtener(self, socio_id: int) -> Socio | None:
        return self.repo.obtener(socio_id)

    def crear(self, datos: SocioBase) -> Socio:
        if self.repo.buscar_por_email(datos.email) is not None:
            raise HTTPException(
                status_code=409, detail="El email ya está registrado"
            )
        return self.repo.crear(datos)

    def actualizar(self, socio_id: int, datos: SocioBase) -> Socio | None:
        socio = self.repo.obtener(socio_id)
        if socio is None:
            return None
        otro = self.repo.buscar_por_email(datos.email)
        if otro is not None and otro.id != socio_id:
            raise HTTPException(
                status_code=409, detail="El email ya está registrado"
            )
        return self.repo.actualizar(socio, datos)

    def eliminar(self, socio_id: int) -> bool:
        socio = self.repo.obtener(socio_id)
        if socio is None:
            return False
        self.repo.eliminar(socio)
        return True