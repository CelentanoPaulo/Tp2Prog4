from fastapi import FastAPI

from models import libros, prestamos, socios  # noqa: F401
from repositories.database import create_db_and_tables
from routers import autores
from routers import libros as libros_router
from routers import prestamos as prestamos_router
from routers import socios as socios_router

app = FastAPI(title="Sistema de Biblioteca")

app.include_router(autores.router)
app.include_router(libros_router.router)
app.include_router(socios_router.router)
app.include_router(prestamos_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "API de Biblioteca funcionando"}