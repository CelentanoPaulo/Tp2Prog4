from datetime import date

from sqlmodel import Field, SQLModel


class PrestamoBase(SQLModel):
    socio_id: int = Field(foreign_key="socio.id")
    libro_id: int = Field(foreign_key="libro.id")


class Prestamo(PrestamoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: date | None = None
    multa: int = 0