from collections.abc import Sequence

from fastapi import HTTPException

from dependencies import AutorRepositoryDep, LibroRepositoryDep
from models.libros import Libro, LibroBase


class LibroService:
    def __init__(
        self, repo: LibroRepositoryDep, autor_repo: AutorRepositoryDep
    ):
        self.repo = repo
        self.autor_repo = autor_repo

    def listar(self, disponibles: bool | None = None) -> Sequence[Libro]:
        return self.repo.listar(disponibles)

    def obtener(self, libro_id: int) -> Libro | None:
        return self.repo.obtener(libro_id)

    def crear(self, datos: LibroBase) -> Libro:
        if self.repo.buscar_por_isbn(datos.isbn) is not None:
            raise HTTPException(
                status_code=409, detail="El ISBN ya está registrado"
            )
        return self.repo.crear(datos)

    def actualizar(self, libro_id: int, datos: LibroBase) -> Libro | None:
        libro = self.repo.obtener(libro_id)
        if libro is None:
            return None
        otro = self.repo.buscar_por_isbn(datos.isbn)
        if otro is not None and otro.id != libro_id:
            raise HTTPException(
                status_code=409, detail="El ISBN ya está registrado"
            )
        return self.repo.actualizar(libro, datos)

    def eliminar(self, libro_id: int) -> bool:
        libro = self.repo.obtener(libro_id)
        if libro is None:
            return False
        self.repo.eliminar(libro)
        return True

    def agregar_autor(self, libro_id: int, autor_id: int) -> Libro:
        libro = self.repo.obtener(libro_id)
        if libro is None:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        autor = self.autor_repo.obtener(autor_id)
        if autor is None:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        if autor in libro.autores:
            raise HTTPException(
                status_code=409, detail="El autor ya está asociado al libro"
            )
        return self.repo.agregar_autor(libro, autor)