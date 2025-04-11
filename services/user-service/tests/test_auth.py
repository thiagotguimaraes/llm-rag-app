import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from app.schemas.user import UserAuthRequest
from app.db.models.user import User
from app.core.security import hash_password, create_access_token

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_db")
async def test_register_user_success(mock_get_db, test_app):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db

    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    mock_db.commit = AsyncMock()

    user_data = {"email": "test@example.com", "password": "password123"}
    response = await AsyncClient(app=test_app, base_url="http://test").post(
        "/register", json=user_data
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    mock_db.add.assert_called_once()

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_db")
async def test_register_user_already_exists(mock_get_db, test_app):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db

    mock_db.execute.return_value.scalars.return_value.first.return_value = User(
        email="test@example.com", hashed_password=hash_password("password123")
    )

    user_data = {"email": "test@example.com", "password": "password123"}
    response = await AsyncClient(app=test_app, base_url="http://test").post(
        "/register", json=user_data
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_db")
async def test_login_user_success(mock_get_db, test_app):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db

    hashed_password = hash_password("password123")
    mock_db.execute.return_value.scalars.return_value.first.return_value = User(
        email="test@example.com", hashed_password=hashed_password
    )

    user_data = {"email": "test@example.com", "password": "password123"}
    response = await AsyncClient(app=test_app, base_url="http://test").post(
        "/login", json=user_data
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_db")
async def test_login_user_invalid_credentials(mock_get_db, test_app):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db

    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    user_data = {"email": "test@example.com", "password": "wrongpassword"}
    response = await AsyncClient(app=test_app, base_url="http://test").post(
        "/login", json=user_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_health_endpoint(test_app):
    response = await AsyncClient(app=test_app, base_url="http://test").get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
@patch("app.api.v1.routes.protected.get_current_user")
async def test_protected_endpoint_success(mock_get_current_user, test_app):
    mock_get_current_user.return_value = {"email": "test@example.com", "role": "user"}

    response = await AsyncClient(app=test_app, base_url="http://test").get("/protected")

    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}

@pytest.mark.asyncio
@patch("app.api.v1.routes.protected.get_current_user")
async def test_protected_endpoint_unauthorized(mock_get_current_user, test_app):
    mock_get_current_user.side_effect = HTTPException(status_code=401, detail="Unauthorized")

    response = await AsyncClient(app=test_app, base_url="http://test").get("/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"