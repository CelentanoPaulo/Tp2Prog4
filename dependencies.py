from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from repositories.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

from repositories.autores import AutorRepository  # noqa: E402
from repositories.libros import LibroRepository  # noqa: E402
from repositories.prestamos import PrestamoRepository  # noqa: E402
from repositories.socios import SocioRepository  # noqa: E402

AutorRepositoryDep = Annotated[AutorRepository, Depends(AutorRepository)]
LibroRepositoryDep = Annotated[LibroRepository, Depends(LibroRepository)]
PrestamoRepositoryDep = Annotated[
    PrestamoRepository, Depends(PrestamoRepository)
]
SocioRepositoryDep = Annotated[SocioRepository, Depends(SocioRepository)]

from services.autores import AutorService  # noqa: E402
from services.libros import LibroService  # noqa: E402
from services.prestamos import PrestamoService  # noqa: E402
from services.socios import SocioService  # noqa: E402

AutorServiceDep = Annotated[AutorService, Depends(AutorService)]
LibroServiceDep = Annotated[LibroService, Depends(LibroService)]
PrestamoServiceDep = Annotated[PrestamoService, Depends(PrestamoService)]
SocioServiceDep = Annotated[SocioService, Depends(SocioService)]