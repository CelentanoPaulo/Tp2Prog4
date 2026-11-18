# TP2 — Sistema de Biblioteca (FastAPI + SQLModel)

API REST para gestionar el catálogo de una biblioteca (autores, libros y socios) y sus préstamos, con reglas de negocio y tests automatizados.

**Alumno:** Paulo Celentano
**Materia:** Programación 4 — TUP, UTN Facultad Regional Paraná

## Tecnologías

- Python 3.13
- FastAPI
- SQLModel (con SQLite)
- pytest + pytest-cov

## Estructura del proyecto

```
Tp2Prog4/
├── models/          # Modelos de datos (tablas y DTOs)
├── repositories/    # Acceso a la base de datos
├── services/        # Reglas de negocio
├── routers/         # Endpoints de la API
├── tests/           # Tests con pytest
├── dependencies.py  # Inyección de dependencias
└── main.py          # Punto de entrada de la aplicación
```

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/CelentanoPaulo/Tp2Prog4.git
cd Tp2Prog4
```

2. Crear y activar el entorno virtual:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Cómo correr la aplicación

```bash
fastapi dev main.py
```

- API: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

La base de datos SQLite (`database.db`) se crea automáticamente al iniciar la aplicación.

## Cómo correr los tests

Los tests usan una base de datos SQLite en memoria, por lo que no modifican `database.db`.

```bash
pytest
```

Para ver la cobertura:

```bash
pytest --cov=. --cov-report=term-missing
```

Cobertura actual: **99 %** (46 tests).

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET / POST | `/autores` | Listar / crear autores |
| GET / PUT / DELETE | `/autores/{id}` | Obtener / modificar / eliminar un autor |
| GET / POST | `/libros` | Listar / crear libros (`?disponibles=true` filtra los que tienen stock) |
| GET / PUT / DELETE | `/libros/{id}` | Obtener / modificar / eliminar un libro |
| POST | `/libros/{id}/autores/{autor_id}` | Asociar un autor a un libro |
| GET / POST | `/socios` | Listar / crear socios |
| GET / PUT / DELETE | `/socios/{id}` | Obtener / modificar / eliminar un socio |
| GET | `/socios/{id}/prestamos` | Préstamos del socio (`?activos=true` solo los activos) |
| GET / POST | `/prestamos` | Listar / registrar préstamos |
| GET | `/prestamos/{id}` | Obtener un préstamo |
| POST | `/prestamos/{id}/devolucion` | Registrar la devolución |

## Reglas de negocio

| # | Regla | Código HTTP |
|---|---|---|
| 1 | Un socio no puede tener más de 3 préstamos activos | 409 |
| 2 | No se presta un libro sin stock; al prestar se descuenta 1 | 409 |
| 3 | Un socio inactivo no puede pedir préstamos | 403 |
| 4 | El plazo es de 14 días (`fecha_vencimiento = fecha_prestamo + 14 días`) | — |
| 5 | Al devolver se repone el stock y se cobra una multa de $100 por día de atraso | — |
| 6 | No se puede devolver un préstamo ya devuelto | 409 |
| 7 | Recurso inexistente | 404 |
| 8 | ISBN o email duplicado | 409 |

Las reglas están implementadas en la capa `services/` y cada una tiene tests del caso exitoso y del caso de error en `tests/`.