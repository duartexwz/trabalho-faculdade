from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.funcoes_auxiliaries import converter_cpf
from api.models import Admin, Alunos
from api.schema_alunos import AlunosFilter, AlunosList, AlunosResponse, AlunosSchemas, AlunosUpdate
from api.schema_cursos import Message
from api.security import get_current_user, get_password_hash

router = APIRouter(prefix="/admin", tags=["admin"])


T_session = Annotated[AsyncSession, Depends(get_session)]
FilterAlunos = Annotated[AlunosFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


router = APIRouter(prefix="/alunos", tags=["alunos"])


@router.post("/", response_model=AlunosResponse, status_code=HTTPStatus.CREATED)
async def cadastrar_alunos(alunos: AlunosSchemas, session: T_session, current_user: CurrentUser):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    aluno_db = await session.scalar(
        select(Alunos).where((Alunos.nome == alunos.nome) | (Alunos.cpf == converter_cpf(alunos.cpf)) | (Alunos.email == alunos.email))
    )

    if aluno_db:
        if aluno_db.nome == alunos.nome:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um aluno cadastrado com esse nome")

        if aluno_db.cpf == alunos.cpf:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um aluno cadastrado com esse CPF")
        if aluno_db.email == alunos.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um aluno cadastrado com esse email")

    aluno_db = Alunos(
        nome=alunos.nome, email=alunos.email, cpf=converter_cpf(alunos.cpf), password=get_password_hash(alunos.password), acesso=alunos.acesso
    )

    session.add(aluno_db)
    await session.commit()
    await session.refresh(aluno_db)

    return aluno_db


@router.get("/", response_model=AlunosList, status_code=HTTPStatus.OK)
async def get_alunos(session: T_session, current_user: CurrentUser, filter_alunos: FilterAlunos):
    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    get_alunos = await session.scalars(select(Alunos).offset(filter_alunos.offset).limit(filter_alunos.limit))

    filtrados = get_alunos.all()

    return {"alunos": filtrados}


@router.patch("/{alunos_id}", response_model=AlunosResponse, status_code=HTTPStatus.OK)
async def uptade_alunos(alunos_id: int, current_user: CurrentUser, session: T_session, alunos: AlunosUpdate):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Premissão negada para esse tipo de ação")

    alunos_db = await session.scalar(select(Alunos).where(Alunos.id == alunos_id))

    if not alunos_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Aluno não encontrado")

    if alunos.nome:
        username_em_uso = await session.scalar(select(Alunos).where(Alunos.nome == alunos.nome, Alunos.id != alunos_id))
        if username_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um aluno com esse nome")

    if alunos.email:
        email_em_uso = await session.scalar(select(Alunos).where(Alunos.email == alunos.email, Admin.id != alunos_id))
        if email_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já tem um aluno com esse email")

    if alunos.cpf:
        cpf_em_uso = await session.scalar(select(Alunos).where(Alunos.cpf == alunos.cpf, Alunos.id != alunos_id))
        if cpf_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um aluno cadastrado com esse CPF")

    for campo, valor in alunos.model_dump(exclude_none=True).items():
        setattr(alunos_db, campo, valor)

    session.add(alunos_db)
    await session.commit()
    await session.refresh(alunos_db)

    return alunos_db


@router.delete("/{alunos_id}", status_code=HTTPStatus.OK, response_model=Message)
async def delete_alunos(session: T_session, current_user: CurrentUser, alunos_id: int):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    alunos_db = await session.scalar(select(Alunos).where(Alunos.id == alunos_id))

    if not alunos_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Aluno não encontrado")

    await session.delete(alunos_db)
    await session.commit()

    return {"message": "Aluno deletado com sucesso!"}
