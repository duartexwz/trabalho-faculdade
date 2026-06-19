from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import admin, alunos, cursos, login, matriculas, usuarios
from api.settings import settings

app = FastAPI(title="Escola Tecno Brasilia", version="1.0.0", redirect_slashes=False)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cursos.router)
app.include_router(login.router)
app.include_router(admin.router)
app.include_router(alunos.router)
app.include_router(matriculas.router)
app.include_router(usuarios.router)
