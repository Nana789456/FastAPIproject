import os
import tempfile
from pathlib import Path

# Переменные окружения нужно задать до импорта app: настройки и engine создаются при импорте
_db_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_db_dir) / 'test.db'}"
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-at-least-32-bytes")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.create_all(engine)
    # https нужен, чтобы клиент отправлял cookie с флагом Secure
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client
    Base.metadata.drop_all(engine)


@pytest.fixture
def logged_in_client(client):
    client.post("/v1/user/", json={"login": "user1", "password": "pass1"})
    response = client.post(
        "/v1/user/login", data={"username": "user1", "password": "pass1"}
    )
    assert response.status_code == 200
    return client
