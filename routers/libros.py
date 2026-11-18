from fastapi import APIRouter, HTTPException

from dependencies import LibroServiceDep
from models.libros import LibroBase, LibroConAutores

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("", response_model=list[LibroConAutores])
def listar_libros(service: LibroServiceDep, disponibles: bool | None = None):
    return service.listar(disponibles)


@router.get("/{libro_id}", response_model=LibroConAutores)
def obtener_libro(libro_id: int, service: LibroServiceDep):
    libro = service.obtener(libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.post("", response_model=LibroConAutores, status_code=201)
def crear_libro(datos: LibroBase, service: LibroServiceDep):
    return service.crear(datos)


@router.put("/{libro_id}", response_model=LibroConAutores)
def actualizar_libro(
    libro_id: int, datos: LibroBase, service: LibroServiceDep
):
    libro = service.actualizar(libro_id, datos)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int, service: LibroServiceDep):
    if not service.eliminar(libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")


@router.post("/{libro_id}/autores/{autor_id}", response_model=LibroConAutores)
def asociar_autor(libro_id: int, autor_id: int, service: LibroServiceDep):
    return service.agregar_autor(libro_id, autor_id)