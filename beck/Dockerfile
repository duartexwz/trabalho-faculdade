FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry config installer.max-workers 10 \
    && poetry install --no-interaction --no-ansi --without dev --no-root

COPY . /app/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]