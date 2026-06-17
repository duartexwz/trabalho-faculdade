from http import HTTPStatus

import factory
import pytest

from api.models import Matriculas


class MatriculaFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Matriculas

    aluno_id = 1
    curso_id = 1
    status = "Ativo"
    nome = factory.Faker("first_name")  # type: ignore
    cpf = factory.Faker("cpf", locale="pt_BR")  # type: ignore
    email = factory.Faker("safe_email")  # type: ignore
    telefone = ("61984092729",)


@pytest.mark.asyncio
async def test_cadastrar_matricula(client, token, cursos, alunos):
    response = await client.post(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "aluno_id": alunos.id,
            "curso_id": cursos.id,
            "status": "Ativo",
            "valor_pago": "100.00",
        },
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "aluno_id": alunos.id,
        "curso_id": cursos.id,
        "status": "Ativo",
        "valor_pago": "100.00",
    }


@pytest.mark.asyncio
async def test_cadastrar_matricula_aluno_nao_encontrado(client, token, cursos):
    response = await client.post(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "aluno_id": 999,
            "curso_id": cursos.id,
            "status": "Ativo",
            "valor_pago": "100.00",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Aluno não encontrado"}


@pytest.mark.asyncio
async def test_cadastrar_matricula_curso_nao_encontrado(client, token, alunos):
    response = await client.post(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "aluno_id": alunos.id,
            "curso_id": 999,
            "status": "Ativo",
            "valor_pago": "100.00",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Curso não encontrado"}


@pytest.mark.asyncio
async def test_cadastrar_matricula_ja_existente(client, token, matricula):
    response = await client.post(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "aluno_id": matricula.aluno_id,
            "curso_id": matricula.curso_id,
            "status": "Ativo",
            "valor_pago": "100.00",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Aluno já matriculado nesse curso"}


@pytest.mark.asyncio
async def test_cadastrar_matricula_permissao_negada(client, token_comum, cursos, alunos):
    response = await client.post(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token_comum}"},
        json={
            "aluno_id": alunos.id,
            "curso_id": cursos.id,
            "status": "Ativo",
            "valor_pago": "100.00",
        },
    )
    # breakpoint()
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Permissão negada para esse tipo de ação"}


@pytest.mark.asyncio
async def test_get_matriculas(client, token, matricula):
    response = await client.get(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["matriculas"]) == 1


@pytest.mark.asyncio
async def test_get_matriculas_filtro_aluno(client, token, matricula):
    response = await client.get(
        f"/matriculas/?aluno_id={matricula.aluno_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["matriculas"][0]["aluno_id"] == matricula.aluno_id


@pytest.mark.asyncio
async def test_get_matriculas_filtro_curso(client, token, matricula):
    response = await client.get(
        f"/matriculas/?curso_id={matricula.curso_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["matriculas"][0]["curso_id"] == matricula.curso_id


@pytest.mark.asyncio
async def test_get_matriculas_filtro_status(client, token, matricula):
    response = await client.get(
        "/matriculas/?status=Ativo",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["matriculas"][0]["status"] == "Ativo"


@pytest.mark.asyncio
async def test_get_matriculas_permissao_negada(client, token_comum):
    response = await client.get(
        "/matriculas/",
        headers={"Authorization": f"Bearer {token_comum}"},
    )
    # breakpoint()

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Permissão negada para esse tipo de ação"}


@pytest.mark.asyncio
async def test_atualizar_matricula(client, token, matricula):
    response = await client.patch(
        f"/matriculas/{matricula.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "Inativo", "valor_pago": "200.00"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "Inativo"
    assert response.json()["valor_pago"] == "200.00"


@pytest.mark.asyncio
async def test_atualizar_matricula_nao_encontrada(client, token):
    response = await client.patch(
        "/matriculas/999",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "Inativo"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Matrícula não encontrada"}


@pytest.mark.asyncio
async def test_atualizar_matricula_curso_nao_encontrado(client, token, matricula):
    response = await client.patch(
        f"/matriculas/{matricula.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"curso_id": 999},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Curso não encontrado"}


@pytest.mark.asyncio
async def test_atualizar_matricula_permissao_negada(client, token_comum, matricula):
    response = await client.patch(
        f"/matriculas/{matricula.id}",
        headers={"Authorization": f"Bearer {token_comum}"},
        json={"status": "Inativo"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Permissão negada para esse tipo de ação"}


@pytest.mark.asyncio
async def test_deletar_matricula(client, token, matricula):
    response = await client.delete(
        f"/matriculas/{matricula.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Matrícula deletada com sucesso!"}


@pytest.mark.asyncio
async def test_deletar_matricula_nao_encontrada(client, token):
    response = await client.delete(
        "/matriculas/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Matrícula não encontrada"}


@pytest.mark.asyncio
async def test_deletar_matricula_permissao_negada(client, token_comum, matricula):
    response = await client.delete(
        f"/matriculas/{matricula.id}",
        headers={"Authorization": f"Bearer {token_comum}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Permissão negada para esse tipo de ação"}
