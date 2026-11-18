from fastapi.testclient import TestClient


def crear_socio(client: TestClient, email: str = "ana@mail.com"):
    response = client.post(
        "/socios", json={"nombre": "Ana", "email": email}
    )
    return response.json()


def test_crear_socio(client: TestClient):
    response = client.post(
        "/socios", json={"nombre": "Ana", "email": "ana@mail.com"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ana@mail.com"
    assert data["activo"] is True


def test_crear_socio_email_duplicado(client: TestClient):
    crear_socio(client, "ana@mail.com")

    response = client.post(
        "/socios", json={"nombre": "Otra", "email": "ana@mail.com"}
    )

    assert response.status_code == 409


def test_listar_socios(client: TestClient):
    crear_socio(client, "ana@mail.com")
    crear_socio(client, "luis@mail.com")

    response = client.get("/socios")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obtener_socio(client: TestClient):
    socio = crear_socio(client)

    response = client.get(f"/socios/{socio['id']}")

    assert response.status_code == 200


def test_obtener_socio_inexistente(client: TestClient):
    response = client.get("/socios/999")

    assert response.status_code == 404


def test_actualizar_socio_manteniendo_su_email(client: TestClient):
    socio = crear_socio(client, "ana@mail.com")

    response = client.put(
        f"/socios/{socio['id']}",
        json={"nombre": "Ana María", "email": "ana@mail.com"},
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Ana María"


def test_actualizar_socio_con_email_de_otro(client: TestClient):
    socio = crear_socio(client, "ana@mail.com")
    crear_socio(client, "luis@mail.com")

    response = client.put(
        f"/socios/{socio['id']}",
        json={"nombre": "Ana", "email": "luis@mail.com"},
    )

    assert response.status_code == 409


def test_actualizar_socio_inexistente(client: TestClient):
    response = client.put(
        "/socios/999", json={"nombre": "X", "email": "x@mail.com"}
    )

    assert response.status_code == 404


def test_eliminar_socio(client: TestClient):
    socio = crear_socio(client)

    response = client.delete(f"/socios/{socio['id']}")

    assert response.status_code == 204


def test_eliminar_socio_inexistente(client: TestClient):
    response = client.delete("/socios/999")

    assert response.status_code == 404