from pydantic import BaseModel, EmailStr


class UsuariosSchemas(BaseModel):
    nome: str
    username: EmailStr
    password: str
    acesso: str


class UsuariosResponse(BaseModel):
    id: int
    nome: str
    username: EmailStr

    acesso: str


class UsuariosDB(UsuariosSchemas):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class UsuariosFilter(BaseModel):
    nome: str | None = None
    username: EmailStr | None = None
    acesso: str | None = None
    offset: int = 0
    limit: int = 10


class UsuariosUpdate(BaseModel):
    nome: str | None = None
    username: EmailStr | None = None
    password: str | None = None
    acesso: str | None = None


class UsuariosList(BaseModel):
    usuarios: list[UsuariosResponse]
