from http import HTTPStatus

import factory
import pytest

from api.models import Cursos


class CursoFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Cursos

    curso = factory.Faker("text")  # type: ignore
    descricao = factory.Faker("text")  # type: ignore
    carga_horaria = factory.Faker("random_int", min=10, max=120)  # type: ignore
    preco = 199.90  # type: ignore
    nivel = factory.Faker("random_element", elements=["Iniciante", "Intermediário", "Avançado"])  # type: ignore
    categoria = factory.Faker("random_element", elements=["Frontend", "Backend", "Full Stack", "Data Science"])  # type: ignore
    imagem = "None"
    status = "Ativo"


@pytest.mark.asyncio
async def test_create_curso(client, token, user_ti):
    response = await client.post(
        "/cursos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "curso": "Engenharia de Software",
            "descricao": "Um dos melhores cursos do brasil na área de TI",
            "carga_horaria": 20,
            "preco": "180.20",
            "nivel": "Intermediário",
            "categoria": "Full Stack",
            "imagem": "None",
            "status": "Ativo",
        },
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "curso": "Engenharia de Software",
        "descricao": "Um dos melhores cursos do brasil na área de TI",
        "carga_horaria": 20,
        "preco": "180.20",
        "nivel": "Intermediário",
        "categoria": "Full Stack",
        "imagem": "None",
        "status": "Ativo",
    }


@pytest.mark.asyncio
async def test_curso_ja_existe(client, cursos, token):
    response = await client.post(
        "/cursos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "curso": "Engenharia de Software",
            "descricao": "Um dos melhores cursos do brasil na área de TI",
            "carga_horaria": 20,
            "preco": "180.20",
            "nivel": "Intermediário",
            "categoria": "Full Stack",
            "imagem": "None",
            "status": "Ativo",
        },
    )

    # breakpoint()

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Este curso já está cadastrado."}


@pytest.mark.asyncio
async def test_get_cursos(client, token):
    response = await client.get(
        "/cursos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"cursos": []}


@pytest.mark.asyncio
async def test_get_cursos_name(client, session, token):

    session.add_all(CursoFactory.create_batch(1, curso="PHP"))

    session.commit()

    response = await client.get(
        "/cursos/?cursos=PHP",
        headers={"Authorization": f"Bearer {token}"},
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json()["cursos"][0]["curso"] == "PHP"


@pytest.mark.asyncio
async def test_atualizar_cursos(client, token, cursos):
    response = await client.patch(
        f"/cursos/{cursos.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "curso": "Python",
            "descricao": "O melhor curso para iniciantes no brasil",
            "carga_horaria": 20,
            "preco": "180.20",
            "nivel": "Intermediário",
            "categoria": "Full Stack",
            "imagem": "None",
            "status": "Ativo",
        },
    )
    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "curso": "Python",
        "descricao": "O melhor curso para iniciantes no brasil",
        "carga_horaria": 20,
        "preco": "180.20",
        "nivel": "Intermediário",
        "categoria": "Full Stack",
        "imagem": "None",
        "status": "Ativo",
    }


@pytest.mark.asyncio
async def test_atualizar_curso_nao_encontrado(client, token):
    response = await client.patch(
        "/cursos/999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "curso": "HTML5",
            "descricao": "O curso front-end mais desenvolvido da atualizade",
            "status": "Ativo",
        },
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Curso não encontrado"}


@pytest.mark.asyncio
async def test_deletar_cuso(client, token, cursos):

    response = await client.delete(f"/cursos/{cursos.id}", headers={"Authorization": f"Bearer {token}"})

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Curso deletado com sucesso!"}


@pytest.mark.asyncio
async def test_deletar_curso_nao_encontrado(client, token):
    response = await client.delete("/cursos/999", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Curso não encontrado"}
