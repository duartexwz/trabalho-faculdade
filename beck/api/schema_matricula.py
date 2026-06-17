from pydantic import BaseModel, EmailStr


class MatriculasSchemas(BaseModel):
    nome: str
    aluno_id: int
    curso_id: int
    status: str
    cpf: str
    telefone: str
    email: EmailStr


class MatriculasResponse(BaseModel):
    id: int
    nome: str
    aluno_id: int
    curso_id: int
    status: str
    cpf: str
    telefone: str
    email: EmailStr


class MatriculasDB(MatriculasSchemas):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class MatriculasFilter(BaseModel):
    nome: str | None = None
    aluno_id: int | None = None
    curso_id: int | None = None
    status: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    offset: int = 0
    limit: int = 10


class MatriculasUpdate(BaseModel):
    nome: str | None = None
    aluno_id: int | None = None
    curso_id: int | None = None
    status: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None


class MatriculasList(BaseModel):
    matriculas: list[MatriculasResponse]
