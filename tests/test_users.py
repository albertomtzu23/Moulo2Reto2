"""Tests del recurso `users`.

Estilo de referencia para nuevos tests:
  - un test por caso, con nombre descriptivo en español
  - arrange / act / assert separados por una línea en blanco
  - se comprueba el status code y lo mínimo del cuerpo que da confianza
"""
from fastapi.testclient import TestClient

from users import repository as users_repository


def test_list_users_devuelve_los_seed(client: TestClient) -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_user_existente_devuelve_200(client: TestClient) -> None:
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["email"] == "ada@example.com"


def test_get_user_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.get("/users/999")

    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


def test_search_user_existente_devuelve_200(client: TestClient) -> None:
    response = client.get("/users/search", params={"email": "ada@example.com"})

    assert response.status_code == 200
    assert response.json()["email"] == "ada@example.com"


def test_search_user_email_invalido_devuelve_422(client: TestClient) -> None:
    response = client.get("/users/search", params={"email": "no-es-un-email"})

    assert response.status_code == 422


def test_search_user_email_vacio_devuelve_422(client: TestClient) -> None:
    response = client.get("/users/search", params={"email": ""})

    assert response.status_code == 422


def test_search_user_sin_email_devuelve_422(client: TestClient) -> None:
    response = client.get("/users/search")

    assert response.status_code == 422


def test_search_user_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.get("/users/search", params={"email": "missing@example.com"})

    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


def test_search_user_email_no_distingue_mayusculas(client: TestClient) -> None:
    response = client.get("/users/search", params={"email": "ADA@EXAMPLE.COM"})

    assert response.status_code == 200
    assert response.json()["email"] == "ada@example.com"


def test_repository_find_by_email_no_distingue_mayusculas() -> None:
    user = users_repository.find_by_email("ADA@EXAMPLE.COM")

    assert user is not None
    assert user.email == "ada@example.com"


def test_create_user_devuelve_201_y_el_usuario(client: TestClient) -> None:
    payload = {"name": "Margaret Hamilton", "email": "margaret@example.com"}

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 5
    assert body["name"] == "Margaret Hamilton"


def test_create_user_email_duplicado_devuelve_409(client: TestClient) -> None:
    payload = {"name": "Otra Ada", "email": "ada@example.com"}

    response = client.post("/users", json=payload)

    assert response.status_code == 409


def test_create_user_email_invalido_devuelve_422(client: TestClient) -> None:
    payload = {"name": "Sin Email", "email": "no-es-un-email"}

    response = client.post("/users", json=payload)

    assert response.status_code == 422
