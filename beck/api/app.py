from fastapi import FastAPI

from api.routers import admin, alunos, cursos, login, matriculas

app = FastAPI(title="Escola Tecno Brasilia", version="1.0.0")

app.include_router(cursos.router)
app.include_router(login.router)
app.include_router(admin.router)
app.include_router(alunos.router)
app.include_router(matriculas.router)
