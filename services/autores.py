from collections.abc import Sequence

from dependencies import AutorRepositoryDep
from models.libros import Autor, AutorBase


class AutorService:
    def __init__(self, repo: AutorRepositoryDep):
        self.repo = repo

    def listar(self) -> Sequence[Autor]:
        return self.repo.listar()

    def obtener(self, autor_id: int) -> Autor | None:
        return self.repo.obtener(autor_id)

    def crear(self, datos: AutorBase) -> Autor:
        return self.repo.crear(datos)

    def actualizar(self, autor_id: int, datos: AutorBase) -> Autor | None:
        autor = self.repo.obtener(autor_id)
        if autor is None:
            return None
        return self.repo.actualizar(autor, datos)

    def eliminar(self, autor_id: int) -> bool:
        autor = self.repo.obtener(autor_id)
        if autor is None:
            return False
        self.repo.eliminar(autor)
        return True