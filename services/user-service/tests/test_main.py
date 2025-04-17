from unittest.mock import AsyncMock, patch
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Required to mock create_async_engine
@pytest.fixture(autouse=True)
def mock_create_async_engine():
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_engine:
        yield mock_engine

def test_main_app_endpoints():
    # Import the app after mocking
    from app.main import app

    # Ensure the app is an instance of FastAPI
    assert isinstance(app, FastAPI)

    # Get all routes in the app
    routes = [route.path for route in app.routes]

    # Assert that the expected endpoints are registered
    assert len(list(filter(lambda x: x.startswith("/api/v1/health/"), routes))) > 0
    assert len(list(filter(lambda x: x.startswith("/api/v1/auth/"), routes))) > 0
    assert len(list(filter(lambda x: x.startswith("/api/v1/protected/"), routes))) > 0