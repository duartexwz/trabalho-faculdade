from pydantic import BaseModel, EmailStr


class AlunosSchemas(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    telefone: str
    status: str


class AlunosResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cpf: str
    telefone: str
    status: str


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
    email: EmailStr | None = None
    cpf: str | None = None
    telefone: str | None = None
    status: str | None = None
    offset: int = 0
    limit: int = 10


class AlunosUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    acesso: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class AlunosList(BaseModel):
    alunos: list[AlunosResponse]
