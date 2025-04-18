import pytest
from httpx import AsyncClient
from app.main import app
from app.db.session import sync_session
from sqlalchemy.sql import text
from httpx._transports.asgi import ASGITransport
from sqlalchemy.future import select
from app.db.session import engine
from app.db.base import Base
from app.db.models.user import User


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_end_to_end_user_workflow():
    with sync_session() as db_session:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # Step 1: Register a new user
            register_payload = {
                "email": "testuser@example.com",
                "password": "securepassword123"
            }
            response = await client.post("/api/v1/auth/register", json=register_payload)
            assert response.status_code == 200
            assert "access_token" in response.json()
            access_token = response.json()["access_token"]

            # Verify the user exists in the database
            result = db_session.execute(
                select(User).where(User.email == "testuser@example.com")
            )
            user = result.scalars().first()
            assert user is not None
            assert user.email == "testuser@example.com"

            # Step 2: Log in with the registered user
            login_payload = {
                "email": "testuser@example.com",
                "password": "securepassword123"
            }
            response = await client.post("/api/v1/auth/login", json=login_payload)
            assert response.status_code == 200
            assert "access_token" in response.json()
            login_token = response.json()["access_token"]

            # Step 3: Access a protected route
            headers = {"Authorization": f"Bearer {login_token}"}
            response = await client.get("/api/v1/protected/me", headers=headers)
            assert response.status_code == 200
            assert response.json()["email"] == "testuser@example.com"


@pytest.mark.asyncio
async def test_admin_workflow():
    with sync_session() as db_session:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # Step 1: Register an admin user
            register_payload = {
                "email": "admin@example.com",
                "password": "adminpassword123",
                # "role": "admin"
            }
            response = await client.post("/api/v1/auth/register", json=register_payload)
            print(response.json())
            assert response.status_code == 200
            admin_token = response.json()["access_token"]

            # Update the user's role to admin directly in the database
            result = db_session.execute(
                select(User).where(User.email == "admin@example.com")
            )
            user = result.scalars().first()
            assert user is not None
            user.role = "admin"
            db_session.commit()

            # Step 2: Access an admin-only route
            headers = {"Authorization": f"Bearer {admin_token}"}
            response = await client.get("/api/v1/protected/admin-only", headers=headers)
            assert response.status_code == 200
            assert response.json()["message"] == "Hello Admin admin@example.com"