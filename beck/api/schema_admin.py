from pydantic import BaseModel, EmailStr


class AdminSchema(BaseModel):
    username: str
    email_admin: EmailStr
    password: str
    acesso: str


class AdminResponse(BaseModel):
    id: int
    username: str
    email_admin: EmailStr
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
    username: str | None = None
    acesso: str | None = None
    email_admin: EmailStr | None = None
    offset: int = 0
    limit: int = 10


class AdminUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    acesso: str | None = None
    email_admin: EmailStr | None = None


class AdminList(BaseModel):
    admin: list[AdminResponse]
