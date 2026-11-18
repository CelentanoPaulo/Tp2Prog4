from sqlmodel import Field, Relationship, SQLModel


class LibroAutor(SQLModel, table=True):
    libro_id: int | None = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    autor_id: int | None = Field(
        default=None, foreign_key="autor.id", primary_key=True
    )


class AutorBase(SQLModel):
    nombre: str = Field(index=True)
    nacionalidad: str


class Autor(AutorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    libros: list["Libro"] = Relationship(
        back_populates="autores", link_model=LibroAutor
    )


class AutorPublic(AutorBase):
    id: int


class LibroBase(SQLModel):
    titulo: str = Field(index=True)
    isbn: str = Field(unique=True)
    stock: int = Field(default=0, ge=0)
    anio: int


class Libro(LibroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autores: list[Autor] = Relationship(
        back_populates="libros", link_model=LibroAutor
    )


class LibroPublic(LibroBase):
    id: int


class LibroConAutores(LibroPublic):
    autores: list[AutorPublic] = []