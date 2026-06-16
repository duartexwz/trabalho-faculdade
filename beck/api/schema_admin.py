from pydantic import BaseModel, EmailStr


class AdminSchema(BaseModel):
    username: EmailStr
    password: str
    acesso: str


class AdminResponse(BaseModel):
    id: int
    username: EmailStr
    acesso: str


class AdminDB(AdminSchema):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class AdminFilter(BaseModel):
    username: EmailStr | None = None
    acesso: str | None = None
    offset: int = 0
    limit: int = 10


class AdminUpdate(BaseModel):
    username: EmailStr | None = None
    password: str | None = None
    acesso: str | None = None


class AdminList(BaseModel):
    admin: list[AdminResponse]
