import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client