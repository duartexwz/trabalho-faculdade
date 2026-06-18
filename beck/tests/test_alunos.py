from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_criar_aluno(client, token):
    response = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Maria Silva",
            "email": "ms.mariasilva@gmail.com",
            "cpf": "715.682.661-11",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "nome": "Maria Silva",
        "email": "ms.mariasilva@gmail.com",
        "cpf": "715.682.661-11",
        "telefone": "0000000-0000",
        "status": "ativo",
    }


@pytest.mark.asyncio
async def test_criar_aluno_nome_ja_existente(client, token):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Mayckon Kenendy",
            "email": "mayckonkennedy877@gmail.com",
            "cpf": "000.000.000-88",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    response = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Mayckon Kenendy",
            "email": "mayckonkennedy977@gmail.com",
            "cpf": "000.000.000-87",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse nome"}


@pytest.mark.asyncio
async def test_criar_aluno_username_ja_existente(client, token):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Joao",
            "email": "mayckonkennedy77@gmail.com",
            "cpf": "500.000.000-84",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    response = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Jose",
            "email": "mayckonkennedy77@gmail.com",
            "cpf": "000.020.000-85",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse email"}


@pytest.mark.asyncio
async def test_criar_aluno_cpf_ja_existente(client, token):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Arthur",
            "email": "felipe@gmail.com",
            "cpf": "666.555.444-33",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    response = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "gabriel",
            "email": "matheus@gmail.com",
            "cpf": "666.555.444-33",
            "telefone": "0000000-0000",
            "status": "ativo",
        },
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse CPF"}


@pytest.mark.asyncio
async def test_get_alunos(client, token, alunos):
    response = await client.get(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "alunos": [
            {
                "id": alunos.id,
                "nome": alunos.nome,
                "email": alunos.email,
                "cpf": alunos.cpf,
                "telefone": alunos.telefone,
                "status": alunos.status,
            }
        ]
    }


@pytest.mark.asyncio
async def test_atualizar_alunos(client, alunos, token):
    response = await client.patch(
        f"/alunos/{alunos.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Welliton Duarte",
            "email": "wellitonduarte@gmail.com",
            "acesso": "Comum",
            "cpf": "000.304.411-45",
            "telefone": alunos.telefone,
            "status": "Ativo",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "nome": "Welliton Duarte",
        "email": "wellitonduarte@gmail.com",
        "cpf": "000.304.411-45",
        "telefone": alunos.telefone,
        "status": "Ativo",
    }


@pytest.mark.asyncio
async def test_atualizar_aluno_nome_existe(client, token, alunos):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno 1",
            "email": "aluno1@teste.com",
            "cpf": "001.303.421-45",
            "telefone": "61984092529",
            "status": "Ativo",
        },
    )

    response_b = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno B",
            "email": "alunoB@teste.com",
            "cpf": "000.304.461-49",
            "telefone": "61984092829",
            "status": "Ativo",
        },
    )

    id_b = response_b.json()["id"]

    response = await client.patch(
        f"/alunos/{id_b}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Aluno 1", "username": "email_b@teste.com", "password": "123", "acesso": "Comum"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse nome"}


@pytest.mark.asyncio
async def test_atualizar_aluno_email_existe(client, token, alunos):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno 1",
            "email": "aluno1@teste.com",
            "cpf": "001.303.421-45",
            "telefone": "61984092529",
            "status": "Ativo",
        },
    )

    response_b = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno B",
            "email": "alunoB@teste.com",
            "cpf": "000.304.461-49",
            "telefone": "61984092829",
            "status": "Ativo",
        },
    )

    id_b = response_b.json()["id"]

    response = await client.patch(
        f"/alunos/{id_b}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Aluno B", "email": "aluno1@teste.com", "password": "123", "acesso": "Comum"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse email"}


@pytest.mark.asyncio
async def test_atualizar_aluno_cpf_existe(client, token, alunos):
    await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno 1",
            "email": "aluno1@teste.com",
            "cpf": "001.303.421-45",
            "telefone": "61984092529",
            "status": "Ativo",
        },
    )

    response_b = await client.post(
        "/alunos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Aluno B",
            "email": "alunoB@teste.com",
            "cpf": "000.304.461-49",
            "telefone": "61984092829",
            "status": "Ativo",
        },
    )

    id_b = response_b.json()["id"]

    response = await client.patch(
        f"/alunos/{id_b}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "Aluno B", "email": "lulamolusculo@teste.com", "cpf": "001.303.421-45", "password": "123", "acesso": "Comum"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um aluno cadastrado com esse CPF"}


@pytest.mark.asyncio
async def test_atualizar_admin(client, token, alunos):
    response = await client.patch(
        f"/alunos/{alunos.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nome": "jose.aaaaaaa", "email": "aluno10@teste.com", "status": "Ativo", "telefone": alunos.telefone, "cpf": "015.658.985-99"},
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "nome": "jose.aaaaaaa",
        "email": "aluno10@teste.com",
        "status": "Ativo",
        "telefone": alunos.telefone,
        "cpf": "015.658.985-99",
    }


@pytest.mark.asyncio
async def test_atualizar_aluno_nao_encontrado(client, token):
    response = await client.patch(
        "/alunos/999",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "duarte@teste.com", "password": "senha", "acesso": "Administrador"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Aluno não encontrado"}


@pytest.mark.asyncio
async def test_deletar_alunos(client, token, alunos):
    response = await client.delete(f"/alunos/{alunos.id}", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Aluno deletado com sucesso!"}


@pytest.mark.asyncio
async def test_delete_aluno_nao_encontrado(client, token):
    response = await client.delete("/alunos/999", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Aluno não encontrado"}
