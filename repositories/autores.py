from collections.abc import Sequence

from sqlmodel import select

from dependencies import SessionDep
from models.libros import Autor, AutorBase


class AutorRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def listar(self) -> Sequence[Autor]:
        return self.session.exec(select(Autor)).all()

    def obtener(self, autor_id: int) -> Autor | None:
        return self.session.get(Autor, autor_id)

    def crear(self, datos: AutorBase) -> Autor:
        autor = Autor.model_validate(datos)
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def actualizar(self, autor: Autor, datos: AutorBase) -> Autor:
        autor.sqlmodel_update(datos.model_dump())
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def eliminar(self, autor: Autor) -> None:
        self.session.delete(autor)
        self.session.commit()