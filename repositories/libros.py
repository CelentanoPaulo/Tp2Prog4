from collections.abc import Sequence

from sqlmodel import select

from dependencies import SessionDep
from models.libros import Autor, Libro, LibroBase


class LibroRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def listar(self, disponibles: bool | None = None) -> Sequence[Libro]:
        statement = select(Libro)
        if disponibles is True:
            statement = statement.where(Libro.stock > 0)
        elif disponibles is False:
            statement = statement.where(Libro.stock == 0)
        return self.session.exec(statement).all()

    def obtener(self, libro_id: int) -> Libro | None:
        return self.session.get(Libro, libro_id)

    def buscar_por_isbn(self, isbn: str) -> Libro | None:
        statement = select(Libro).where(Libro.isbn == isbn)
        return self.session.exec(statement).first()

    def crear(self, datos: LibroBase) -> Libro:
        libro = Libro.model_validate(datos)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def actualizar(self, libro: Libro, datos: LibroBase) -> Libro:
        libro.sqlmodel_update(datos.model_dump())
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def eliminar(self, libro: Libro) -> None:
        self.session.delete(libro)
        self.session.commit()

    def agregar_autor(self, libro: Libro, autor: Autor) -> Libro:
        libro.autores.append(autor)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro