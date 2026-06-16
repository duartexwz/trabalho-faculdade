from decimal import Decimal

from pydantic import BaseModel


class MatriculasSchemas(BaseModel):
    aluno_id: int
    curso_id: int
    status: str
    valor_pago: Decimal


class MatriculasResponse(BaseModel):
    id: int
    aluno_id: int
    curso_id: int
    status: str
    valor_pago: Decimal


class MatriculasDB(MatriculasSchemas):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class MatriculasFilter(BaseModel):
    aluno_id: int | None = None
    curso_id: int | None = None
    status: str | None = None
    valor_pago: Decimal | None = None
    offset: int = 0
    limit: int = 10


class MatriculasUpdate(BaseModel):
    aluno_id: int | None = None
    curso_id: int | None = None
    status: str | None = None
    valor_pago: Decimal | None = None


class MatriculasList(BaseModel):
    matriculas: list[MatriculasResponse]
