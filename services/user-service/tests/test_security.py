from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest
from app.db.models.user import User
from fastapi import HTTPException
from jose import jwt


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


@pytest.mark.asyncio
@patch("app.core.security.get_sync_session")
@patch("app.core.security.JWT_SECRET_KEY", "mock_secret_key")
@patch("app.core.security.JWT_ALGORITHM", "mock_algorithm")
@patch("app.core.security.jwt.decode")
async def test_get_current_user_success(mock_jwt_decode, mock_get_sync_session):
    from app.core.security import get_current_user

    # Mock database session
    mock_db_session = Mock()
    mock_get_sync_session.return_value = mock_db_session

    # Mock user in database
    mock_user = User(id=1, email="test@example.com", role="user", is_active=True)
    mock_db_session.execute.return_value = mock_query_result(mock_user)

    # Call the function
    token = "mock_token"
    result = get_current_user(token=token, db=mock_db_session)

    # Assertions
    assert result == mock_user
    mock_jwt_decode.assert_called_once_with(
        token, "mock_secret_key", algorithms=["mock_algorithm"]
    )
    mock_db_session.execute.assert_called_once()


@pytest.mark.asyncio
@patch("app.core.security.get_sync_session")
@patch("app.core.security.jwt.decode")
async def test_get_current_user_invalid_token(mock_jwt_decode, mock_get_sync_session):
    from app.core.security import get_current_user

    # Mock JWT decode to raise an error
    mock_jwt_decode.side_effect = jwt.JWTError

    # Mock database session
    mock_db_session = Mock()
    mock_get_sync_session.return_value = mock_db_session

    # Call the function and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid_token", db=mock_db_session)

    # Assertions
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid authentication credentials"
    mock_jwt_decode.assert_called_once()


def test_hash_password():
    from app.core.security import hash_password

    # Call the function
    hashed_password = hash_password("password123")

    # Assertions
    assert hashed_password != "password123"  # Ensure the password is hashed


def test_verify_password():
    from app.core.security import hash_password, verify_password

    # Hash a password
    hashed_password = hash_password("password123")

    # Call the function
    assert verify_password("password123", hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


@patch("app.core.security.JWT_SECRET_KEY", "mock_secret_key")
@patch("app.core.security.JWT_ALGORITHM", "mock_algorithm")
@patch("app.core.security.datetime")
@patch("app.core.security.jwt.encode")
def test_create_access_token(mock_jwt_encode, mock_datetime):
    from app.core.security import create_access_token

    mock_datetime_utcnow = datetime(2023, 1, 1)
    mock_datetime.utcnow.return_value = mock_datetime_utcnow

    # Mock user
    mock_user = User(id=1, email="test@example.com", role="user")

    mock_jwt_encode.return_value = "mock_token"

    # Call the function
    token = create_access_token(mock_user, expires_delta=timedelta(minutes=15))
    assert token == "mock_token"
    mock_jwt_encode.assert_called_once_with(
        {
            "sub": str(mock_user.id),
            "email": mock_user.email,
            "role": mock_user.role,
            "exp": mock_datetime_utcnow + timedelta(minutes=15),
        },
        "mock_secret_key",
        algorithm="mock_algorithm",
    )


@pytest.mark.asyncio
async def test_require_role_success():
    from app.core.security import require_role

    # Mock user
    mock_user = User(id=1, email="test@example.com", role="admin")

    # Call the function
    role_checker = require_role("admin")
    result = role_checker(user=mock_user)

    # Assertions
    assert result == mock_user


@pytest.mark.asyncio
async def test_require_role_forbidden():
    from app.core.security import require_role

    # Mock user
    mock_user = User(id=1, email="test@example.com", role="user")

    # Call the function and expect an exception
    role_checker = require_role("admin")
    with pytest.raises(HTTPException) as exc_info:
        role_checker(user=mock_user)

    # Assertions
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Forbidden: insufficient role"
