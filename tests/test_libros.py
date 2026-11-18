from fastapi.testclient import TestClient


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


def crear_autor(client: TestClient):
    response = client.post(
        "/autores", json={"nombre": "Cortázar", "nacionalidad": "Argentina"}
    )
    return response.json()


def test_crear_libro(client: TestClient):
    response = client.post(
        "/libros",
        json={"titulo": "Rayuela", "isbn": "111", "stock": 2, "anio": 1963},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["isbn"] == "111"
    assert data["autores"] == []


def test_crear_libro_isbn_duplicado(client: TestClient):
    crear_libro(client, isbn="111")

    response = client.post(
        "/libros",
        json={"titulo": "Otro", "isbn": "111", "stock": 1, "anio": 2000},
    )

    assert response.status_code == 409


def test_crear_libro_stock_negativo(client: TestClient):
    response = client.post(
        "/libros",
        json={"titulo": "X", "isbn": "999", "stock": -1, "anio": 2000},
    )

    assert response.status_code == 422


def test_listar_libros_disponibles(client: TestClient):
    crear_libro(client, isbn="111", stock=2)
    crear_libro(client, isbn="222", stock=0)

    todos = client.get("/libros")
    disponibles = client.get("/libros", params={"disponibles": True})
    sin_stock = client.get("/libros", params={"disponibles": False})

    assert len(todos.json()) == 2
    assert len(disponibles.json()) == 1
    assert disponibles.json()[0]["isbn"] == "111"
    assert len(sin_stock.json()) == 1
    assert sin_stock.json()[0]["isbn"] == "222"


def test_obtener_libro(client: TestClient):
    libro = crear_libro(client)

    response = client.get(f"/libros/{libro['id']}")

    assert response.status_code == 200


def test_obtener_libro_inexistente(client: TestClient):
    response = client.get("/libros/999")

    assert response.status_code == 404


def test_actualizar_libro(client: TestClient):
    libro = crear_libro(client, isbn="111")

    response = client.put(
        f"/libros/{libro['id']}",
        json={"titulo": "Rayuela", "isbn": "111", "stock": 5, "anio": 1963},
    )

    assert response.status_code == 200
    assert response.json()["stock"] == 5


def test_actualizar_libro_con_isbn_de_otro(client: TestClient):
    libro = crear_libro(client, isbn="111")
    crear_libro(client, isbn="222")

    response = client.put(
        f"/libros/{libro['id']}",
        json={"titulo": "Rayuela", "isbn": "222", "stock": 2, "anio": 1963},
    )

    assert response.status_code == 409


def test_actualizar_libro_inexistente(client: TestClient):
    response = client.put(
        "/libros/999",
        json={"titulo": "X", "isbn": "999", "stock": 1, "anio": 2000},
    )

    assert response.status_code == 404


def test_eliminar_libro(client: TestClient):
    libro = crear_libro(client)

    response = client.delete(f"/libros/{libro['id']}")

    assert response.status_code == 204


def test_eliminar_libro_inexistente(client: TestClient):
    response = client.delete("/libros/999")

    assert response.status_code == 404


def test_asociar_autor_a_libro(client: TestClient):
    libro = crear_libro(client)
    autor = crear_autor(client)

    response = client.post(f"/libros/{libro['id']}/autores/{autor['id']}")

    assert response.status_code == 200
    autores = response.json()["autores"]
    assert len(autores) == 1
    assert autores[0]["nombre"] == "Cortázar"


def test_asociar_autor_dos_veces(client: TestClient):
    libro = crear_libro(client)
    autor = crear_autor(client)
    client.post(f"/libros/{libro['id']}/autores/{autor['id']}")

    response = client.post(f"/libros/{libro['id']}/autores/{autor['id']}")

    assert response.status_code == 409


def test_asociar_autor_inexistente(client: TestClient):
    libro = crear_libro(client)

    response = client.post(f"/libros/{libro['id']}/autores/999")

    assert response.status_code == 404


def test_asociar_autor_a_libro_inexistente(client: TestClient):
    autor = crear_autor(client)

    response = client.post(f"/libros/999/autores/{autor['id']}")

    assert response.status_code == 404