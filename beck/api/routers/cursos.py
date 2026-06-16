from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin, Cursos
from api.schema_cursos import (
    CursosFilter,
    CursosList,
    CursosResponse,
    CursosSchema,
    CursosUpdate,
    Message,
)
from api.security import get_current_user

router = APIRouter(prefix="/cursos", tags=["cursos"])


T_session = Annotated[AsyncSession, Depends(get_session)]
FilterCursos = Annotated[CursosFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/", response_model=CursosResponse, status_code=HTTPStatus.CREATED)
async def create_curso(session: T_session, curso: CursosSchema, current_user: CurrentUser):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    cursos_db = await session.scalar(select(Cursos).where(Cursos.curso == curso.curso))

    if cursos_db:
        if cursos_db.curso == curso.curso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Este curso já está cadastrado.")

    cursos_db = Cursos(
        curso=curso.curso,
        descricao=curso.descricao,
        carga_horaria=curso.carga_horaria,
        preco=curso.preco,
        nivel=curso.nivel,
        categoria=curso.categoria,
        imagem=curso.imagem,
        status=curso.status,
    )

    session.add(cursos_db)
    await session.commit()
    await session.refresh(cursos_db)

    return cursos_db


@router.get("/", response_model=CursosList, status_code=HTTPStatus.OK)
async def get_cursos(session: T_session, filter_cursos: FilterCursos, current_user: CurrentUser):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    query = select(Cursos)

    if filter_cursos.curso:
        query = query.where(Cursos.curso.ilike(f"{filter_cursos.curso}%"))

    get_cursos = await session.scalars(select(Cursos).offset(filter_cursos.offset).limit(filter_cursos.limit))

    filtrados = get_cursos.all()

    return {"cursos": filtrados}


@router.patch("/{curso_id}", response_model=CursosResponse, status_code=HTTPStatus.OK)
async def update_cursos(session: T_session, current_user: CurrentUser, curso_id: int, curso: CursosUpdate):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    cursos_db = await session.scalar(select(Cursos).where((Cursos.id == curso_id)))

    if not cursos_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Curso não encontrado")

    for campo, valor in curso.model_dump(exclude_none=True).items():
        setattr(cursos_db, campo, valor)

    session.add(cursos_db)
    await session.commit()
    await session.refresh(cursos_db)

    return cursos_db


@router.delete("/{curso_id}", response_model=Message, status_code=HTTPStatus.OK)
async def delete_curso(session: T_session, current_user: CurrentUser, curso_id: int):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    curso_db = await session.scalar(select(Cursos).where(Cursos.id == curso_id))

    if not curso_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Curso não encontrado")

    await session.delete(curso_db)
    await session.commit()

    return {"message": "Curso deletado com sucesso!"}
