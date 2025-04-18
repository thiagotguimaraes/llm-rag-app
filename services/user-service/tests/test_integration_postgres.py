import psycopg2
import pytest
from psycopg2 import OperationalError
from app.config import db_connection_params


@pytest.fixture
def postgres_connection():
    try:
        connection = psycopg2.connect(**db_connection_params)
        yield connection
    finally:
        if connection:
            connection.close()


def test_postgres_health(postgres_connection):
    try:
        cursor = postgres_connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        assert result == (1,), "Postgres health check failed"
    except OperationalError as e:
        pytest.fail(f"Postgres connection failed: {e}")
