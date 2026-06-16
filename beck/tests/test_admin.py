from http import HTTPStatus

import factory
import pytest

from api.models import Admin


class AdminFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Admin

    username = factory.Faker("name")  # type: ignore

    @factory.sequence  # type: ignore
    def email_admin(n):
        return f"admin{n}@info.com"

    acesso = "Administrador"
    password = "admin.admin"


@pytest.mark.asyncio
async def test_create_admin(client, token):
    response = await client.post(
        "/admin/",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "mayckon.duarte", "email_admin": "mayckon@info.com", "password": "my_secret_key", "acesso": "Administrador"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 2, "username": "mayckon.duarte", "email_admin": "mayckon@info.com", "acesso": "Administrador"}


@pytest.mark.asyncio
async def test_username_admin_ja_existe(client, token, admin_teste_2):
    response = await client.post(
        "/admin/",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Admin", "email_admin": "mayckon2@info.com", "password": "admin.admin", "acesso": "Administrador"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um administrador com esse username"}


@pytest.mark.asyncio
async def test_email_ja_existe(client, token, admin_teste_2):
    response = await client.post(
        "/admin/",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Admin2", "email_admin": "admin2@info.com", "password": "admin.admin", "acesso": "Administrador"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um administrador com esse username"}


@pytest.mark.asyncio
async def test_get_admin(client, token, user_ti):
    response = await client.get(
        "/admin/",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "admin": [
            {
                "id": user_ti.id,
                "email_admin": user_ti.email_admin,
                "username": user_ti.username,
                "acesso": user_ti.acesso,
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_admin_name(client, session, token, user_ti):

    session.add_all(AdminFactory.create_batch(1, username="Admin Falso"))

    await session.commit()

    response = await client.get(
        "/admin/?username=Admin Falso",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json()["admin"][0]["username"] == user_ti.username


@pytest.mark.asyncio
async def test_atualizar_admin(client, token, user_ti):
    response = await client.patch(
        f"/admin/{user_ti.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "jose.aaaaaaa", "email_admin": "admin10@teste.com", "password": "my_secret_key", "acesso": "Administrador"},
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "jose.aaaaaaa", "email_admin": "admin10@teste.com", "acesso": "Administrador"}


@pytest.mark.asyncio
async def test_atualizar_admin_nao_encontrado(client, token):
    response = await client.patch(
        "/admin/999",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "duarte.teste", "password": "senha", "acesso": "Administrador"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Administrador não encontrado"}


@pytest.mark.asyncio
async def test_deletar_admin(client, token, admin_teste):
    response = await client.delete(f"/admin/{admin_teste.id}", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Administrador deletado com sucesso!"}


@pytest.mark.asyncio
async def test_deletar_admin_nao_encontrado(client, token):
    response = await client.delete(
        "/admin/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Administrador não encontrado"}
