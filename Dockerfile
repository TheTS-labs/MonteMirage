# syntax=docker/dockerfile:1.4
FROM python:alpine3.17
WORKDIR /app

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk update && apk upgrade && \
    apk add chromium chromium-chromedriver

COPY [ "./poetry.lock", "./pyproject.toml", "./" ]

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry run poetry install

COPY ./ ./

ENTRYPOINT [ "poetry", "run", "python3", "Parser.py" ]