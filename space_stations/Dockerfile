FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY ./ ./

ENV BASE_NAME=1

CMD ['gunicorn', 'space_stations.wsgi:application', '--bind', '0:8000']