from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from repositories.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

from repositories.autores import AutorRepository  # noqa: E402

AutorRepositoryDep = Annotated[AutorRepository, Depends(AutorRepository)]

from services.autores import AutorService  # noqa: E402

AutorServiceDep = Annotated[AutorService, Depends(AutorService)]