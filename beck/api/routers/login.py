from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin, Usuarios
from api.schema_cursos import (
    CursosFilter,
    Token,
)
from api.security import create_access_token, get_current_user, verify_password

router = APIRouter(prefix="/login", tags=["login"], redirect_slashes=False)

T_session = Annotated[AsyncSession, Depends(get_session)]
FilterCursos = Annotated[CursosFilter, Query()]
CurrentUser = Annotated[Admin, Depends(get_current_user)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/", response_model=Token, status_code=HTTPStatus.OK)
async def login_for_access_token(session: T_session, form_data: Oauth2Form):
    user = await session.scalar(select(Admin).where(Admin.username == form_data.username))

    if not user:
        user = await session.scalar(select(Usuarios).where(Usuarios.username == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect email or password")

    identifier = getattr(user, "username", None) or getattr(user, "nome", None)
    access_token = await create_access_token(data={"sub": identifier})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh_login", response_model=Token)
async def refreash_access_token(current_user: CurrentUser):

    identifier = getattr(current_user, "username", None) or getattr(current_user, "nome", None)
    new_access_token = await create_access_token(data={"sub": identifier})

    return {"access_token": new_access_token, "token_type": "bearer"}
