import psycopg2
import pytest
from psycopg2 import OperationalError

@pytest.fixture
def postgres_connection():
    # Replace with your PostgreSQL connection details
    connection_params = {
        "dbname": "test_db",
        "user": "test_user",
        "password": "test_pass",
        "host": "localhost",
        "port": 5432,
    }
    try:
        connection = psycopg2.connect(**connection_params)
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