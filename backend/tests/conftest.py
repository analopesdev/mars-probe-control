import os
import sqlite3
import tempfile

# O banco de teste precisa ser definido antes de importar a aplicação.
TEST_DB = os.path.join(tempfile.mkdtemp(), "test_probe.db")
os.environ["DATABASE_PATH"] = TEST_DB

import pytest
from fastapi.testclient import TestClient

from database import init_db
from main import app
from repositories.probe_repository import ProbeRepository
from services.probe_service import ProbeService


@pytest.fixture
def service(tmp_path):
    """Service com um banco SQLite novo, sem passar pela API."""
    database_path = str(tmp_path / "probe.db")
    init_db(database_path)
    return ProbeService(ProbeRepository(database_path))


@pytest.fixture
def client():
    """Cliente HTTP da API, com a tabela de sondas vazia a cada teste."""
    with TestClient(app) as test_client:
        with sqlite3.connect(TEST_DB) as connection:
            connection.execute("DELETE FROM probes")
        yield test_client
