from fastapi.testclient import TestClient


def crear_autor(client: TestClient, nombre: str = "Borges"):
    response = client.post(
        "/autores", json={"nombre": nombre, "nacionalidad": "Argentina"}
    )
    return response.json()


def test_crear_autor(client: TestClient):
    response = client.post(
        "/autores", json={"nombre": "Borges", "nacionalidad": "Argentina"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nombre"] == "Borges"


def test_listar_autores(client: TestClient):
    crear_autor(client, "Borges")
    crear_autor(client, "Cortázar")

    response = client.get("/autores")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obtener_autor(client: TestClient):
    autor = crear_autor(client)

    response = client.get(f"/autores/{autor['id']}")

    assert response.status_code == 200
    assert response.json()["nombre"] == "Borges"


def test_obtener_autor_inexistente(client: TestClient):
    response = client.get("/autores/999")

    assert response.status_code == 404


def test_actualizar_autor(client: TestClient):
    autor = crear_autor(client)

    response = client.put(
        f"/autores/{autor['id']}",
        json={"nombre": "Borges", "nacionalidad": "Suiza"},
    )

    assert response.status_code == 200
    assert response.json()["nacionalidad"] == "Suiza"


def test_actualizar_autor_inexistente(client: TestClient):
    response = client.put(
        "/autores/999", json={"nombre": "X", "nacionalidad": "Y"}
    )

    assert response.status_code == 404


def test_eliminar_autor(client: TestClient):
    autor = crear_autor(client)

    response = client.delete(f"/autores/{autor['id']}")

    assert response.status_code == 204
    assert client.get(f"/autores/{autor['id']}").status_code == 404


def test_eliminar_autor_inexistente(client: TestClient):
    response = client.delete("/autores/999")

    assert response.status_code == 404