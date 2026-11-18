from collections.abc import Sequence

from sqlmodel import select

from dependencies import SessionDep
from models.socios import Socio, SocioBase


class SocioRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def listar(self) -> Sequence[Socio]:
        return self.session.exec(select(Socio)).all()

    def obtener(self, socio_id: int) -> Socio | None:
        return self.session.get(Socio, socio_id)

    def buscar_por_email(self, email: str) -> Socio | None:
        statement = select(Socio).where(Socio.email == email)
        return self.session.exec(statement).first()

    def crear(self, datos: SocioBase) -> Socio:
        socio = Socio.model_validate(datos)
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def actualizar(self, socio: Socio, datos: SocioBase) -> Socio:
        socio.sqlmodel_update(datos.model_dump())
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def eliminar(self, socio: Socio) -> None:
        self.session.delete(socio)
        self.session.commit()