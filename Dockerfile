FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip "poetry==1.8.2"
RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .