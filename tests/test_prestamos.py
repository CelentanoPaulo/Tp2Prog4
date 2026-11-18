from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlmodel import Session

from models.prestamos import Prestamo


def crear_socio(
    client: TestClient, email: str = "ana@mail.com", activo: bool = True
):
    response = client.post(
        "/socios",
        json={"nombre": "Ana", "email": email, "activo": activo},
    )
    return response.json()


def crear_libro(client: TestClient, isbn: str = "111", stock: int = 2):
    response = client.post(
        "/libros",
        json={
            "titulo": "Rayuela",
            "isbn": isbn,
            "stock": stock,
            "anio": 1963,
        },
    )
    return response.json()


def prestar(client: TestClient, socio_id: int, libro_id: int):
    return client.post(
        "/prestamos", json={"socio_id": socio_id, "libro_id": libro_id}
    )


# Regla 2 y 4: préstamo exitoso, descuenta stock y vence en 14 días
def test_prestamo_exitoso(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client, stock=2)

    response = prestar(client, socio["id"], libro["id"])

    assert response.status_code == 201
    data = response.json()
    hoy = date.today()
    assert data["fecha_prestamo"] == hoy.isoformat()
    assert data["fecha_vencimiento"] == (hoy + timedelta(days=14)).isoformat()
    assert data["fecha_devolucion"] is None
    assert data["multa"] == 0
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 1


# Regla 2: no se presta un libro sin stock
def test_prestamo_sin_stock(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client, stock=0)

    response = prestar(client, socio["id"], libro["id"])

    assert response.status_code == 409


# Regla 3: un socio inactivo no puede pedir préstamos
def test_prestamo_socio_inactivo(client: TestClient):
    socio = crear_socio(client, activo=False)
    libro = crear_libro(client)

    response = prestar(client, socio["id"], libro["id"])

    assert response.status_code == 403


# Regla 1: máximo 3 préstamos activos
def test_maximo_tres_prestamos_activos(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client, stock=10)

    for _ in range(3):
        assert prestar(client, socio["id"], libro["id"]).status_code == 201

    response = prestar(client, socio["id"], libro["id"])

    assert response.status_code == 409


# Regla 7: recursos inexistentes
def test_prestamo_socio_inexistente(client: TestClient):
    libro = crear_libro(client)

    response = prestar(client, 999, libro["id"])

    assert response.status_code == 404


def test_prestamo_libro_inexistente(client: TestClient):
    socio = crear_socio(client)

    response = prestar(client, socio["id"], 999)

    assert response.status_code == 404


# Regla 5: devolución a tiempo, sin multa y repone stock
def test_devolucion_a_tiempo(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client, stock=2)
    prestamo = prestar(client, socio["id"], libro["id"]).json()

    response = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert response.status_code == 200
    data = response.json()
    assert data["fecha_devolucion"] == date.today().isoformat()
    assert data["multa"] == 0
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 2


# Regla 5: devolución con 3 días de atraso, multa de $300
def test_devolucion_con_atraso(client: TestClient, session: Session):
    socio = crear_socio(client)
    libro = crear_libro(client)
    prestamo_id = prestar(client, socio["id"], libro["id"]).json()["id"]

    prestamo = session.get(Prestamo, prestamo_id)
    assert prestamo is not None
    prestamo.fecha_vencimiento = date.today() - timedelta(days=3)
    session.add(prestamo)
    session.commit()

    response = client.post(f"/prestamos/{prestamo_id}/devolucion")

    assert response.status_code == 200
    assert response.json()["multa"] == 300


# Regla 6: no se puede devolver un préstamo ya devuelto
def test_devolver_dos_veces(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client)
    prestamo = prestar(client, socio["id"], libro["id"]).json()
    client.post(f"/prestamos/{prestamo['id']}/devolucion")

    response = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert response.status_code == 409


def test_devolver_prestamo_inexistente(client: TestClient):
    response = client.post("/prestamos/999/devolucion")

    assert response.status_code == 404


def test_prestamos_activos_del_socio(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client, stock=5)
    primero = prestar(client, socio["id"], libro["id"]).json()
    prestar(client, socio["id"], libro["id"])
    client.post(f"/prestamos/{primero['id']}/devolucion")

    url = f"/socios/{socio['id']}/prestamos"
    todos = client.get(url)
    activos = client.get(url, params={"activos": True})
    devueltos = client.get(url, params={"activos": False})

    assert len(todos.json()) == 2
    assert len(activos.json()) == 1
    assert len(devueltos.json()) == 1


def test_prestamos_de_socio_inexistente(client: TestClient):
    response = client.get("/socios/999/prestamos")

    assert response.status_code == 404


def test_listar_y_obtener_prestamos(client: TestClient):
    socio = crear_socio(client)
    libro = crear_libro(client)
    prestamo = prestar(client, socio["id"], libro["id"]).json()

    assert len(client.get("/prestamos").json()) == 1
    assert client.get(f"/prestamos/{prestamo['id']}").status_code == 200
    assert client.get("/prestamos/999").status_code == 404