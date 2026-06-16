from pydantic import BaseModel, EmailStr


class AlunosSchemas(BaseModel):
    nome: str
    username: EmailStr
    cpf: str
    acesso: str
    password: str


class AlunosResponse(BaseModel):
    id: int
    nome: str
    username: EmailStr
    acesso: str
    cpf: str


class AlunosDB(AlunosSchemas):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class AlunosFilter(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    acesso: str | None = None
    username: EmailStr | None = None
    offset: int = 0
    limit: int = 10


class AlunosUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    acesso: str | None = None
    username: EmailStr | None = None
    password: str | None = None


class AlunosList(BaseModel):
    alunos: list[AlunosResponse]
