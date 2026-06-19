from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.models import Admin, Usuarios
from api.settings import Settings

settings = Settings()  # type: ignore
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
Token = Annotated[str, Depends(Oauth2_scheme)]
T_session = Annotated[AsyncSession, Depends(get_session)]
password_hash = PasswordHash.recommended()


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encode_jwt = encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encode_jwt


async def get_current_user(token: Token, session: T_session):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_error = HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permissão negada para esse tipo de ação")

    try:
        payload = decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        subject_email = payload.get("sub")

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(select(Admin).where(Admin.username == subject_email))

    if not user:
        user = await session.scalar(select(Usuarios).where(Usuarios.username == subject_email))

    if not user:
        raise credentials_exception

    if user.acesso != "Administrador":
        raise access_error

    return user


def verify_password(hashed_password, plain_password):
    return password_hash.verify(hashed_password, plain_password)


def get_password_hash(password):
    return password_hash.hash(password)
