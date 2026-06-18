from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal

import factory
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from api.app import app
from api.database import get_session
from api.models import Admin, Alunos, Cursos, Matriculas, Usuarios, table_registry
from api.security import get_password_hash


class UserTiFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Admin

    username = factory.Faker("safe_email")  # type: ignore
    password = "admin.admin"
    acesso = "Administrador"


class AlunosFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Alunos

    nome = factory.Faker("first_name")  # type: ignore
    email = factory.Faker("safe_email")  # type: ignore
    cpf = "012.954.852-99"
    telefone = factory.Faker("numerify", locale="pt_BR", text="%%9%%%%%%%%")  # type: ignore
    status = "Ativo"


class UsuariosFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Usuarios

    nome = factory.Faker("first_name")  # type: ignore
    username = factory.Faker("safe_email")  # type: ignore
    password = "usuarios.comum"
    acesso = "Comum"


class OutrosAlunosFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Alunos

    nome = factory.Faker("first_name")  # type: ignore
    email = factory.Faker("safe_email")  # type: ignore
    cpf = "022.953.842-98"
    telefone = factory.Faker("numerify", locale="pt_BR", text="%%9%%%%%%%%")  # type: ignore
    status = "Ativo"


@pytest_asyncio.fixture
async def client(session):
    async def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "update_at"):
            target.update_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user_ti(session):
    password = "admin.admin"
    user = UserTiFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


@pytest_asyncio.fixture
async def admin_teste(session):
    admin = Admin(username="admin@info.com", password=get_password_hash("admin.admin"), acesso="Comum")

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def admin_teste_2(session):
    admin = Admin(username="admin2@info.com", password=get_password_hash("admin.admin"), acesso="Administrador")

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def alunos(session):
    password = "aluno.123"
    aluno = AlunosFactory()

    session.add(aluno)
    await session.commit()
    await session.refresh(aluno)

    aluno.clean_password = password
    return aluno


@pytest_asyncio.fixture
async def outros_alunos(session):
    password = "aluno.123"
    outro_aluno = OutrosAlunosFactory()

    session.add(outro_aluno)
    await session.commit()
    await session.refresh(outro_aluno)

    outro_aluno.clean_password = password
    return outro_aluno


@pytest_asyncio.fixture
async def cursos(session):
    curso = Cursos(
        curso="Engenharia de Software",
        descricao="O melhor curso de Ti da atualidade",
        carga_horaria=20,
        preco=Decimal("180.20"),
        nivel="Intermediário",
        categoria="Full Stack",
        imagem="None",
        status="Ativo",
    )

    session.add(curso)
    await session.commit()
    await session.refresh(curso)

    return curso


@pytest_asyncio.fixture
async def outros_cursos(session):
    outro_curso = Cursos(
        curso="PHP com MySQL",
        descricao="O melhor curso de banco de dados da atualidade",
        carga_horaria=20,
        preco=Decimal("180.20"),
        nivel="Intermediário",
        categoria="Banco de dados",
        imagem="None",
        status="Ativo",
    )

    session.add(outro_curso)
    await session.commit()
    await session.refresh(outro_curso)

    return outro_curso


@pytest_asyncio.fixture
async def token(client, user_ti):
    response = await client.post("/login/", data={"username": user_ti.username, "password": user_ti.clean_password})

    # breakpoint()
    print(response.json())
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def usuarios(session):
    password = "usuarios.comum"
    usuario = UsuariosFactory(password=get_password_hash(password))

    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)

    usuario.clean_password = password
    return usuario


@pytest_asyncio.fixture
async def token_comum(client, usuarios):
    response = await client.post("/login/", data={"username": usuarios.username, "password": usuarios.clean_password})

    # breakpoint()
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def matricula(session, alunos, cursos):
    matricula = Matriculas(
        aluno_id=alunos.id,
        curso_id=cursos.id,
        status="Ativo",
        nome="Teste",
        cpf="000.018.365-99",
        email="matricula1000@teste.com",
        telefone="61984092729",
    )
    session.add(matricula)
    await session.commit()
    await session.refresh(matricula)
    return matricula


@pytest_asyncio.fixture
async def outra_matricula(session, outros_alunos, outros_cursos):
    matricula = Matriculas(
        aluno_id=outros_alunos.id,
        curso_id=outros_cursos.id,
        status="Ativo",
        nome="Teste 2",
        cpf="012.698.365-99",
        email="matricula@teste.com",
        telefone="62984092729",
    )
    session.add(matricula)
    await session.commit()
    await session.refresh(matricula)
    return matricula
