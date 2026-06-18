from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_cadastrar_usuario(client, token):
    response = await client.post(
        "/usuarios/",
        headers={"Authorization": "Bearer"},
        json={"nome": "usuario", "username": "usuario@username.com", "password": "usuario.password", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "nome": "usuario", "username": "usuario@username.com", "acesso": "Comum"}


@pytest.mark.asyncio
async def test_cadastrar_usuario_nome_existe(client, token):
    await client.post(
        "/usuarios/",
        headers={"Authorization": "Bearer"},
        json={"nome": "usuario", "username": "usuario1@username.com", "password": "usuario.password", "acesso": "Comum"},
    )

    response = await client.post(
        "/usuarios/",
        headers={"Authorization": "Bearer"},
        json={"nome": "usuario", "username": "usuario2@username.com", "password": "usuario.password", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um usuario cadastrado com esse nome"}


@pytest.mark.asyncio
async def test_usuario_username_ja_existe(client, token):
    await client.post(
        "/usuarios/",
        headers={"Authorization": "Bearer"},
        json={"nome": "usuario 1 ", "username": "usuario@username.com", "password": "usuario.password", "acesso": "Comum"},
    )

    response = await client.post(
        "/usuarios/",
        headers={"Authorization": "Bearer"},
        json={"nome": "usuario 2 ", "username": "usuario@username.com", "password": "usuario.password", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um usuario cadastrado com esse email"}


@pytest.mark.asyncio
async def test_get_usuarios(client, token, usuarios):
    response = await client.get(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"usuarios": [{"id": usuarios.id, "nome": usuarios.nome, "username": usuarios.username, "acesso": "Comum"}]}


@pytest.mark.asyncio
async def test_atualizar_usuarios(client, usuarios, token):
    response = await client.patch(
        f"/usuarios/{usuarios.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Welliton Duarte", "username": "wellitonduarte@gmail.com", "password": "update.teste", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "nome": "Welliton Duarte", "username": "wellitonduarte@gmail.com", "acesso": "Comum"}


@pytest.mark.asyncio
async def test_atualizar_usuario_username_ja_existe(client, token):
    await client.post(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario A", "username": "email_original@teste.com", "password": "123", "acesso": "Comum"},
    )

    response_b = await client.post(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario B", "username": "email_b@teste.com", "password": "123", "acesso": "Comum"},
    )
    id_b = response_b.json()["id"]

    response = await client.patch(
        f"/usuarios/{id_b}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario B Editado", "username": "email_original@teste.com", "password": "123", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um usuario cadastrado com esse email"}


@pytest.mark.asyncio
async def test_atualizar_usuario_nome_existe(client, token, usuarios):
    await client.post(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario A", "username": "email_original@teste.com", "password": "123", "acesso": "Comum"},
    )

    response_b = await client.post(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario B", "username": "email_b@teste.com", "password": "123", "acesso": "Comum"},
    )
    id_b = response_b.json()["id"]

    response = await client.patch(
        f"/usuarios/{id_b}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario A", "username": "email_b@teste.com", "password": "123", "acesso": "Comum"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um usuario cadastrado com esse nome"}


@pytest.mark.asyncio
async def test_usuario_nao_encontrado(client, token):
    response = await client.patch(
        "usuarios/0000",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Usuario A", "username": "email_b@teste.com", "password": "123", "acesso": "Comum"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Usuário não encontrado"}


@pytest.mark.asyncio
async def test_deletar_usuarios(client, token, usuarios):
    response = await client.delete(f"/usuarios/{usuarios.id}", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Usuário deletado com sucesso!"}


@pytest.mark.asyncio
async def test_deletar_usuarios_nao_encontrado(
    client,
    token,
):
    response = await client.delete("/usuarios/999", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Usuário não encontrado"}
