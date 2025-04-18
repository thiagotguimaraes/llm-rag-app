import psycopg2
import pytest
from psycopg2 import OperationalError
from app.config import db_connection_params
import time


@pytest.fixture
def postgres_connection():
    
    db_connection_params["host"] = "localhost"
    print("connection_params", db_connection_params)
    
    max_retries = 5
    retry_delay = 2
    connection = None

    for attempt in range(max_retries):
        try:
            connection = psycopg2.connect(**db_connection_params)
            yield connection
            break
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                pytest.fail(f"Postgres connection failed after {max_retries} attempts: {e}")
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
