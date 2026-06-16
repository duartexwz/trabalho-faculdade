from decimal import Decimal

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class CursosSchema(BaseModel):
    curso: str
    descricao: str
    carga_horaria: int
    preco: Decimal
    nivel: str
    categoria: str
    imagem: str
    status: str


class CursosResponse(BaseModel):
    id: int
    curso: str
    descricao: str
    carga_horaria: int
    nivel: str
    categoria: str
    preco: Decimal
    imagem: str
    status: str


class CursosList(BaseModel):
    cursos: list[CursosResponse]


class CursosDB(CursosSchema):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class CursosFilter(BaseModel):
    curso: str | None = None
    descricao: str | None = None
    status: str | None = None
    carga_horaria: int | None = None
    nivel: str | None = None
    categoria: str | None = None
    offset: int = 0
    limit: int = 10


class CursosUpdate(BaseModel):
    curso: str | None = None
    descricao: str | None = None
    status: str | None = None
    carga_horaria: int | None = None
    nivel: str | None = None
    categoria: str | None = None
