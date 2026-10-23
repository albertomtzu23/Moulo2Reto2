# m2-api-base

API REST de usuarios usada como base en el **Módulo 2 · Clase 1 — Generación de código con IA**.

Es un proyecto pequeño y ejecutable con convenciones, capas separadas, catálogo
de errores y una suite de tests. Incluye búsqueda de usuarios por email en
`GET /users/search`.

## Requisitos

- Python 3.10 o superior
- (Recomendado) Claude Code instalado

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
uvicorn main:app --reload          # http://127.0.0.1:8000  ·  Swagger en /docs
```

Endpoints actuales:

| Método | Ruta              | Descripción                     |
|--------|-------------------|---------------------------------|
| GET    | `/health`         | Estado del servicio             |
| GET    | `/users`          | Lista de usuarios               |
| GET    | `/users/search?email=<email>` | Busca un usuario por email (422 si el formato es inválido, 404 si no existe) |
| GET    | `/users/{id}`     | Un usuario por id (404 si no existe) |
| POST   | `/users`          | Crea un usuario (409 si el email ya existe) |

### Buscar usuario por email

Ejemplo de solicitud:

```bash
curl "http://127.0.0.1:8000/users/search?email=ada%40example.com"
```

- **200 OK:** devuelve el objeto `User` si el email existe.
- **422 Unprocessable Entity:** el parámetro `email` falta o no tiene un formato válido.
- **404 Not Found:** el email tiene formato válido, pero no corresponde a ningún usuario.

## Tests y calidad

```bash
pytest                                       # correr la suite
pytest --cov=. --cov-report=term-missing     # con cobertura
ruff check .                                 # linter
```

La implementación sigue el flujo ruta → servicio → repositorio. Las pruebas de
aceptación y casos límite están en `tests/test_users.py`.

## Evidencias del Reto 2

- [Log del proceso, changelog y reflexión](./Reto2-Evidencias/clase5-log-proceso.md)
- [Prompts y reflexión del uso de IA](./Reto2-Evidencias/clase5-prompts.md)

Lee `CLAUDE.md` antes de empezar: ahí están las convenciones que tu código debe respetar.
