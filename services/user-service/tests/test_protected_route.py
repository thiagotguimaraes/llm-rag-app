from unittest.mock import Mock, patch

import pytest


# Required to mock create_async_engine
@pytest.fixture(autouse=True)
def mock_create_async_engine():
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_engine:
        yield mock_engine


@pytest.mark.asyncio
async def test_read_my_profile():
    from app.api.v1.routes.protected import read_my_profile

    # Mock the current user
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.role = "user"

    # Call the function
    result = read_my_profile(user=mock_user)

    # Assertions
    assert result == {"id": 1, "email": "test@example.com", "role": "user"}


@pytest.mark.asyncio
async def test_admin_endpoint():
    from app.api.v1.routes.protected import admin_endpoint

    # Mock the admin user
    mock_user = Mock()
    mock_user.email = "admin@example.com"
    # mock_require_role.return_value = lambda role: mock_user

    # Call the function
    result = admin_endpoint(user=mock_user)

    # Assertions
    assert result == {"message": "Hello Admin admin@example.com"}
