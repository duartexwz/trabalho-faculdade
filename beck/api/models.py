from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Cursos:
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    curso: Mapped[str] = mapped_column(unique=True)
    descricao: Mapped[str] = mapped_column()
    carga_horaria: Mapped[int] = mapped_column(nullable=False)
    preco: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    nivel: Mapped[str] = mapped_column(nullable=False)
    categoria: Mapped[str] = mapped_column(nullable=False)
    imagem: Mapped[Optional[str]] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, init=False, server_onupdate=func.now(), nullable=True)


@table_registry.mapped_as_dataclass
class Admin:
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    acesso: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, init=False, server_onupdate=func.now(), nullable=True)


@table_registry.mapped_as_dataclass
class Alunos:
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(unique=True, nullable=False)
    cpf: Mapped[str] = mapped_column(unique=True)
    telefone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, init=False, server_onupdate=func.now(), nullable=True)


@table_registry.mapped_as_dataclass
class Usuarios:
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)
    acesso: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, init=False, server_onupdate=func.now(), nullable=True)


@table_registry.mapped_as_dataclass
class Matriculas:
    __tablename__ = "matriculas"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(unique=True, nullable=False)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id", ondelete="CASCADE"))
    data_matricula: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    cpf: Mapped[str] = mapped_column(unique=True)
    telefone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str] = mapped_column(nullable=False)
