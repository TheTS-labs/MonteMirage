# syntax=docker/dockerfile:1.4
FROM python:alpine3.17
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY [ "./poetry.lock", "./pyproject.toml", "./" ]

RUN poetry run poetry install

COPY ./ ./

ENTRYPOINT [ "poetry", "run", "python3", "main.py" ]