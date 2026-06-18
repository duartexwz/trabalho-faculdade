from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin, Usuarios
from api.schema_cursos import Message
from api.schemas_usuarios import UsuariosFilter, UsuariosList, UsuariosResponse, UsuariosSchemas, UsuariosUpdate
from api.security import get_current_user, get_password_hash

T_session = Annotated[AsyncSession, Depends(get_session)]
Filterusuarios = Annotated[UsuariosFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuariosResponse, status_code=HTTPStatus.CREATED)
async def cadastrar_usuarios(usuarios: UsuariosSchemas, session: T_session):

    usuario_db = await session.scalar(select(Usuarios).where((Usuarios.nome == usuarios.nome) | (Usuarios.username == usuarios.username)))

    if usuario_db:
        if usuario_db.nome == usuarios.nome:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario cadastrado com esse nome")

        if usuario_db.username == usuarios.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario cadastrado com esse email")

    usuario_db = Usuarios(nome=usuarios.nome, username=usuarios.username, password=get_password_hash(usuarios.password), acesso=usuarios.acesso)

    session.add(usuario_db)
    await session.commit()
    await session.refresh(usuario_db)

    return usuario_db


@router.get("/", response_model=UsuariosList, status_code=HTTPStatus.OK)
async def get_usuarios(session: T_session, filter_usuarios: Filterusuarios):

    get_usuarios = await session.scalars(select(Usuarios).offset(filter_usuarios.offset).limit(filter_usuarios.limit))

    filtrados = get_usuarios.all()

    return {"usuarios": filtrados}


@router.patch("/{usuarios_id}", response_model=UsuariosResponse, status_code=HTTPStatus.OK)
async def uptade_usuarios(usuarios_id: int, session: T_session, usuarios: UsuariosUpdate):
    usuarios_db = await session.scalar(select(Usuarios).where(Usuarios.id == usuarios_id))

    if not usuarios_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    if usuarios.nome:
        nome_em_uso = await session.scalar(select(Usuarios).where(Usuarios.nome == usuarios.nome, Usuarios.id != usuarios_id))
        if nome_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario cadastrado com esse nome")

    if usuarios.username:
        username_em_uso = await session.scalar(select(Usuarios).where(Usuarios.username == usuarios.username, Admin.id != usuarios_id))
        if username_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario cadastrado com esse email")

    for campo, valor in usuarios.model_dump(exclude_none=True).items():
        setattr(usuarios_db, campo, valor)

    session.add(usuarios_db)
    await session.commit()
    await session.refresh(usuarios_db)

    return usuarios_db


@router.delete("/{usuarios_id}", response_model=Message)
async def delete_usuarios(session: T_session, current_user: CurrentUser, usuarios_id: int):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    usuarios_db = await session.scalar(select(Usuarios).where(Usuarios.id == usuarios_id))

    # breakpoint()
    if not usuarios_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    await session.delete(usuarios_db)
    await session.commit()

    return {"message": "Usuário deletado com sucesso!"}
