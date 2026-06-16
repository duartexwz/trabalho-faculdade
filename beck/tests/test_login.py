from http import HTTPStatus

import pytest
from freezegun import freeze_time


@pytest.mark.asyncio
async def test_token(client, user_ti):
    response = await client.post("/login/", data={"username": user_ti.username, "password": "admin.admin"})
    # breakpoint()
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_username_nao_autorizado(client):
    payload = {"username": "teste", "password": "secret"}

    response = await client.post("/login/", data=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_senha_nao_autorizado(client, admin_teste):
    payload = {"username": "Admin", "password": "admin.123456"}

    response = await client.post("/login/", data=payload)

    # breakpoint()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_criar_curso_permissao_negada(client, session, admin_teste):

    session.add(admin_teste)
    await session.commit()
    await session.refresh(admin_teste)

    login = await client.post(
        "/login/",
        data={"username": admin_teste.username, "password": "admin.admin", "acesso": "Comum"},
    )
    # breakpoint()
    token = login.json()["access_token"]

    response = await client.post(
        "/cursos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "curso": "Curso de desenvolvimento Web",
            "descricao": "Melhor curso web do mundo",
            "status": "Inativo",
        },
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Permissão negada para esse tipo de ação"}


@pytest.mark.asyncio
async def test_token_expiret_after_time(client, user_ti):
    with freeze_time("2026-06-16 11:10"):
        response = await client.post(
            "/login/",
            data={"username": user_ti.username, "password": user_ti.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2026-06-16 11:41"):
        response = await client.patch(
            f"/admin/{user_ti.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@email.com",
                "password": "wrongTeste",
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


@pytest.mark.asyncio
async def test_token_inexistent_user(client):
    response = await client.post("/login/", data={"username": "no@user.com", "password": "testtest"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_token_wrong_password(client, user_ti):
    response = await client.post("/login/", data={"username": user_ti.username, "password": "wrong_password"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_refresh_token(client, token):
    response = await client.post(
        "/login/refresh_login",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    # breakpoint()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_token_expired_dont_refresh(client, user_ti):
    with freeze_time("2023-07-14 12:00:00"):
        response = await client.post(
            "/login/",
            data={"username": user_ti.username, "password": user_ti.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = await client.post(
            "/login/refresh_login",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
