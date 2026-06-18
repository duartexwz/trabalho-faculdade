from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin, Cursos, Matriculas
from api.schema_cursos import Message
from api.schema_matricula import (
    MatriculasFilter,
    MatriculasList,
    MatriculasResponse,
    MatriculasSchemas,
    MatriculasUpdate,
)
from api.security import get_current_user

router = APIRouter(prefix="/matriculas", tags=["matriculas"])

T_session = Annotated[AsyncSession, Depends(get_session)]
FilterMatriculas = Annotated[MatriculasFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]


@router.post("/", response_model=MatriculasResponse, status_code=HTTPStatus.CREATED)
async def cadastrar_matricula(matricula: MatriculasSchemas, session: T_session):

    matricula_existente = await session.scalar(
        select(Matriculas).where((Matriculas.aluno_id == matricula.aluno_id) & (Matriculas.curso_id == matricula.curso_id))
    )

    if matricula_existente:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Aluno já matriculado nesse curso")

    matricula_db = Matriculas(
        aluno_id=matricula.aluno_id,
        curso_id=matricula.curso_id,
        status=matricula.status,
        cpf=matricula.cpf,
        telefone=matricula.telefone,
        email=matricula.email,
        nome=matricula.nome,
    )

    session.add(matricula_db)
    await session.commit()
    await session.refresh(matricula_db)

    return matricula_db


@router.get("/", response_model=MatriculasList, status_code=HTTPStatus.OK)
async def get_matriculas(session: T_session, filter_matriculas: FilterMatriculas):

    query = select(Matriculas)

    if filter_matriculas.aluno_id:
        query = query.where(Matriculas.aluno_id == filter_matriculas.aluno_id)

    if filter_matriculas.curso_id:
        query = query.where(Matriculas.curso_id == filter_matriculas.curso_id)

    if filter_matriculas.status:
        query = query.where(Matriculas.status == filter_matriculas.status)

    matriculas = await session.scalars(query.offset(filter_matriculas.offset).limit(filter_matriculas.limit))

    return {"matriculas": matriculas.all()}


@router.patch("/{matricula_id}", response_model=MatriculasResponse, status_code=HTTPStatus.OK)
async def update_matricula(matricula_id: int, session: T_session, matricula: MatriculasUpdate):

    matricula_db = await session.scalar(select(Matriculas).where(Matriculas.id == matricula_id))

    if not matricula_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Matrícula não encontrada")

    if matricula.curso_id:
        curso_db = await session.scalar(select(Cursos).where(Cursos.id == matricula.curso_id))
        if not curso_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Curso não encontrado")

        matricula_existente = await session.scalar(
            select(Matriculas).where((Matriculas.aluno_id == matricula_db.aluno_id) & (Matriculas.curso_id == matricula.curso_id))
        )
        if matricula_existente:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Aluno já matriculado nesse curso")

    for campo, valor in matricula.model_dump(exclude_none=True).items():
        setattr(matricula_db, campo, valor)

    session.add(matricula_db)
    await session.commit()
    await session.refresh(matricula_db)

    return matricula_db


@router.delete("/{matricula_id}", status_code=HTTPStatus.OK, response_model=Message)
async def delete_matricula(session: T_session, current_user: CurrentUser, matricula_id: int):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    matricula_db = await session.scalar(select(Matriculas).where(Matriculas.id == matricula_id))

    if not matricula_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Matrícula não encontrada")

    await session.delete(matricula_db)
    await session.commit()

    return {"message": "Matrícula deletada com sucesso!"}
