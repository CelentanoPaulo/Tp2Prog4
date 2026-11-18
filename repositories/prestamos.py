from collections.abc import Sequence

from sqlmodel import col, select

from dependencies import SessionDep
from models.libros import Libro
from models.prestamos import Prestamo


class PrestamoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def listar(self) -> Sequence[Prestamo]:
        return self.session.exec(select(Prestamo)).all()

    def obtener(self, prestamo_id: int) -> Prestamo | None:
        return self.session.get(Prestamo, prestamo_id)

    def listar_por_socio(
        self, socio_id: int, activos: bool | None = None
    ) -> Sequence[Prestamo]:
        statement = select(Prestamo).where(Prestamo.socio_id == socio_id)
        devolucion = col(Prestamo.fecha_devolucion)
        if activos is True:
            statement = statement.where(devolucion.is_(None))
        elif activos is False:
            statement = statement.where(devolucion.is_not(None))
        return self.session.exec(statement).all()

    def guardar(self, prestamo: Prestamo, libro: Libro) -> Prestamo:
        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo