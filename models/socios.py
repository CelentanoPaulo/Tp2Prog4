from sqlmodel import Field, SQLModel


class SocioBase(SQLModel):
    nombre: str
    email: str = Field(unique=True)
    activo: bool = True


class Socio(SocioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)