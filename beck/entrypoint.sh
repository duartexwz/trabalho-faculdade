#!/bin/sh

echo "Aguradando o banco de dados iniciar..."

sleep 5

echo "Rodando as migrações e o upgrade head..."

poetry run alembic upgrade head


echo "Iniciando o uvicorn"
poetry run uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload