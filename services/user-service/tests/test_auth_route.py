from unittest.mock import Mock, AsyncMock, patch
import pytest
from fastapi import HTTPException, FastAPI

from app.schemas.user import UserAuthRequest
from app.db.models.user import User

# Required to mock create_async_engine
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

def test_login_endpoint_registered():
    # Import the router after everything is mocked
    from app.api.v1.routes.auth import router
    # Create a FastAPI app and include the auth router
    app = FastAPI()
    app.include_router(router)

    # Get all routes in the app
    routes = [[route.path, route.methods] for route in app.routes]

    # Assert that the /login endpoint is registered
    assert ["/login", {'POST'}] in routes

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
@patch("app.api.v1.routes.auth.verify_password")
@patch("app.api.v1.routes.auth.create_access_token")
async def test_login_success(mock_create_access_token, mock_verify_password, mock_get_async_session):
    # Import the router after everything is mocked
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
    # Import the router after everything is mocked
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
    # Import the router after everything is mocked
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


def test_register_endpoint_registered():
    # Import the router after everything is mocked
    from app.api.v1.routes.auth import router
    # Create a FastAPI app and include the auth router
    app = FastAPI()
    app.include_router(router)

    # Get all routes in the app
    routes = [[route.path, route.methods] for route in app.routes]

    # Assert that the /register endpoint is registered
    assert ["/register", {'POST'}] in routes


@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
@patch("app.api.v1.routes.auth.hash_password")
@patch("app.api.v1.routes.auth.create_access_token")
async def test_register_success(mock_create_access_token, mock_hash_password, mock_get_async_session):
    # Import the router after everything is mocked
    from app.api.v1.routes.auth import register
    # Mock dependencies
    mock_db_session = AsyncMock()
    mock_get_async_session.return_value = mock_db_session
    mock_hash_password.return_value = "hashed_password"
    mock_create_access_token.return_value = "mock_token"

    # Mock database query for existing user
    mock_db_session.execute.return_value = mock_query_result(mock_user=None)

    # Test data
    user_in = UserAuthRequest(email="test@example.com", password="password123")

    # Call the function
    result = await register(user_in, db=mock_db_session)

    # Assertions
    assert result.access_token == "mock_token"
    mock_hash_password.assert_called_once_with("password123")
    mock_create_access_token.assert_called_once()
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
@patch("app.api.v1.routes.auth.get_async_session")
async def test_register_user_already_exists(mock_get_async_session):
    # Import the router after everything is mocked
    from app.api.v1.routes.auth import register
    # Mock dependencies
    mock_db_session = AsyncMock()
    mock_get_async_session.return_value = mock_db_session

    # Mock database query for existing user
    mock_user = User(email="test@example.com", hashed_password="hashed_password")
    mock_db_session.execute.return_value = mock_query_result(mock_user)

    # Test data
    user_in = UserAuthRequest(email="test@example.com", password="password123")

    # Call the function and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        await register(user_in, db=mock_db_session)

    # Assertions
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User already exists"
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()