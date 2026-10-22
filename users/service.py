"""Lógica de negocio del recurso `users`.

Las rutas no acceden al repositorio directamente: pasan por aquí. Esta capa es la
única que conoce `repository.py` y la que decide cuándo algo es un error de
dominio (usando `core.errors`).
"""
from core import errors
from users import repository
from users.schemas import User, UserCreate


def _require_user(user: User | None, identifier: int | str) -> User:
    if user is None:
        raise errors.not_found("usuario", identifier)
    return user


def get_user(user_id: int) -> User:
    return _require_user(repository.get(user_id), user_id)


def list_users() -> list[User]:
    return repository.list_all()


def search_user(email: str) -> User:
    """Busca por email sin distinguir mayúsculas y minúsculas."""
    return _require_user(repository.find_by_email(email), email)


def create_user(data: UserCreate) -> User:
    if repository.find_by_email(str(data.email)) is not None:
        raise errors.already_exists("usuario", data.email)
    return repository.add(name=data.name, email=str(data.email))
