from fastapi import FastAPI

from repositories.database import create_db_and_tables

from models import libros, prestamos, socios 

app = FastAPI(title="Sistema de Biblioteca")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "API de Biblioteca funcionando"}