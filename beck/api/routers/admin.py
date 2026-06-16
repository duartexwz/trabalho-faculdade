from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin
from api.schema_admin import AdminFilter, AdminList, AdminResponse, AdminSchema, AdminUpdate
from api.schema_cursos import Message
from api.security import get_current_user, get_password_hash

router = APIRouter(prefix="/admin", tags=["admin"])


T_session = Annotated[AsyncSession, Depends(get_session)]
FilterAdmin = Annotated[AdminFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AdminResponse)
async def create_admin(admin: AdminSchema, current_user: CurrentUser, session: T_session):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    admin_db = await session.scalar(select(Admin).where((Admin.username == admin.username) | (Admin.email_admin == admin.email_admin)))

    if admin_db:
        if admin_db.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um administrador com esse username")

        if admin_db.email_admin:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já tem um adinistrador com esse email")

    admin_db = Admin(username=admin.username, email_admin=admin.email_admin, password=get_password_hash(admin.password), acesso=admin.acesso)

    session.add(admin_db)
    await session.commit()
    await session.refresh(admin_db)

    return admin_db


@router.get("/", status_code=HTTPStatus.OK, response_model=AdminList)
async def get_admin(session: T_session, filter_admin: FilterAdmin, current_user: CurrentUser):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")
    get_admin = await session.scalars(select(Admin).offset(filter_admin.offset).limit(filter_admin.limit))

    filtrados = get_admin.all()

    return {"admin": filtrados}


@router.patch("/{admin_id}", response_model=AdminResponse, status_code=HTTPStatus.OK)
async def update_admin(admin_id: int, session: T_session, current_user: CurrentUser, admin: AdminUpdate):
    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    admin_db = await session.scalar(select(Admin).where(Admin.id == admin_id))

    if not admin_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Administrador não encontrado")

    if admin.username:
        username_em_uso = await session.scalar(select(Admin).where(Admin.username == admin.username, Admin.id != admin_id))
        if username_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um administrador com esse username")

    if admin.email_admin:
        email_em_uso = await session.scalar(select(Admin).where(Admin.email_admin == admin.email_admin, Admin.id != admin_id))
        if email_em_uso:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já tem um adinistrador com esse email")

    for campo, valor in admin.model_dump(exclude_none=True).items():
        setattr(admin_db, campo, valor)

    session.add(admin_db)
    await session.commit()
    await session.refresh(admin_db)

    return admin_db


@router.delete("/{admin_id}", status_code=HTTPStatus.OK, response_model=Message)
async def delete_admin(session: T_session, current_user: CurrentUser, admin_id: int):

    if current_user.acesso != "Administrador":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    admin_db = await session.scalar(select(Admin).where(Admin.id == admin_id))

    if not admin_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Administrador não encontrado")

    await session.delete(admin_db)
    await session.commit()

    return {"message": "Administrador deletado com sucesso!"}
