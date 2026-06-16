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
from api.models import Admin, Alunos, Cursos, Matriculas, table_registry
from api.security import get_password_hash


class UserTiFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Admin

    username = factory.Faker("first_name")  # type: ignore
    email_admin = factory.Faker("safe_email")  # type: ignore
    password = "admin.admin"
    acesso = "Administrador"


class AlunosFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Alunos

    nome = factory.Faker("first_name")  # type: ignore
    email = factory.Faker("safe_email")  # type: ignore
    cpf = "012.954.852-99"
    password = "aluno.123"
    acesso = "Comum"


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
    admin = Admin(username="Admin", email_admin="admin@info.com", password=get_password_hash("admin.admin"), acesso="Comum")

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def admin_teste_2(session):
    admin = Admin(username="Admin", email_admin="admin2@info.com", password=get_password_hash("admin.admin"), acesso="Administrador")

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def alunos(session):
    password = "aluno.123"
    aluno = AlunosFactory(password=get_password_hash(password))

    session.add(aluno)
    await session.commit()
    await session.refresh(aluno)

    aluno.clean_password = password
    return aluno


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
async def token(client, user_ti):
    response = await client.post("/login", data={"username": user_ti.username, "password": user_ti.clean_password})

    # breakpoint()
    print(response.json())
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def token_comum(client, alunos):
    response = await client.post("/login", data={"username": alunos.nome, "password": alunos.clean_password})

    print(response.json)
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def matricula(session, alunos, cursos):
    matricula = Matriculas(
        aluno_id=alunos.id,
        curso_id=cursos.id,
        status="Ativo",
        valor_pago=Decimal("100.00"),
    )
    session.add(matricula)
    await session.commit()
    await session.refresh(matricula)
    return matricula
