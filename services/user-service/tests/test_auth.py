from unittest.mock import Mock, AsyncMock, patch
import pytest
from fastapi import HTTPException

from app.schemas.user import UserAuthRequest
from app.db.models.user import User

# required to mock create_async_engine and don't deal with DATABASE_URL env variable
@pytest.fixture(autouse=True)
def mock_create_async_engine():
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_engine:
        yield mock_engine

# Mock database query for user
def mock_query_result(mock_user):
    mock_scalars = Mock()
    mock_scalars.first.return_value = mock_user
    mock_result = Mock()
    mock_result.scalars.return_value = mock_scalars
    return mock_result

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
@patch("app.api.v1.routes.auth.verify_password")
@patch("app.api.v1.routes.auth.create_access_token")
async def test_login_success(mock_create_access_token, mock_verify_password, mock_get_async_session):
    from app.api.v1.routes.auth import login
    # Mock dependencies
    mock_db_session = AsyncMock()
    mock_get_async_session.return_value = mock_db_session
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "mock_token"

    # Mock database query for user
    mock_user = User(email="test@example.com", hashed_password="hashed_password")
    mock_db_session.execute.return_value = mock_query_result(mock_user)

    # Test data
    user_in = UserAuthRequest(email="test@example.com", password="password123")

    # Call the function
    result = await login(user_in, db=mock_db_session)

    # Assertions
    assert result.access_token == "mock_token"
    mock_verify_password.assert_called_once_with("password123", "hashed_password")
    mock_create_access_token.assert_called_once_with(mock_user)

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
@patch("app.api.v1.routes.auth.verify_password")
async def test_login_invalid_credentials(mock_verify_password, mock_get_async_session):
    from app.api.v1.routes.auth import login
    # Mock dependencies
    mock_db_session = AsyncMock()
    mock_get_async_session.return_value = mock_db_session
    mock_verify_password.return_value = False

    # Mock database query for user
    mock_db_session.execute.return_value = mock_query_result(User(email="test@example.com", hashed_password="hashed_password"))

    # Test data
    user_in = UserAuthRequest(email="test@example.com", password="wrongpassword")

    # Call the function and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        await login(user_in, db=mock_db_session)

    # Assertions
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"
    mock_verify_password.assert_called_once_with("wrongpassword", "hashed_password")

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
async def test_login_user_not_found(mock_get_async_session):
    from app.api.v1.routes.auth import login
    # Mock dependencies
    mock_db_session = AsyncMock()
    mock_get_async_session.return_value = mock_db_session

    # Mock database query for user
    mock_db_session.execute.return_value = mock_query_result(mock_user=None)

    # Test data
    user_in = UserAuthRequest(email="nonexistent@example.com", password="password123")

    # Call the function and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        await login(user_in, db=mock_db_session)

    # Assertions
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"