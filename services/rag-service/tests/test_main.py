# import pytest
# from unittest.mock import AsyncMock, patch
# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock
# from fastapi import FastAPI

# # # Required to mock create_async_engine
# @pytest.fixture(autouse=True)
# def mock_create_async_engine():
#     with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_async_engine:
#         yield mock_async_engine

# @pytest.fixture(autouse=True)
# def mock_create_engine():
#     with patch("sqlalchemy.create_engine") as mock_engine:
#         yield mock_engine

# @pytest.fixture(autouse=True)
# def mock_OpenAI():
#     with patch("openai.OpenAI") as mock_OpenAI:
#         yield mock_OpenAI

# @pytest.fixture(autouse=True)
# def mock_QdrantClient():
#     with patch("qdrant_client.QdrantClient") as mock_QdrantClient:
#         yield mock_QdrantClient

# # Mock the individual route modules
# @patch("app.api.v1.routes.health", )
# @patch("app.api.v1.routes.upload")
# @patch("app.api.v1.routes.search")
# @patch("app.api.v1.routes.rag")
# def test_routes(mock_health_router, mock_upload_router, mock_search_router, mock_rag_router):
#     from app.main import app

#     # Mock the routers' behavior if necessary
#     mock_health_router.router = MagicMock()
#     mock_upload_router.router = MagicMock()
#     mock_search_router.router = MagicMock()
#     mock_rag_router.router = MagicMock()

#     # Ensure the app is an instance of FastAPI
#     assert isinstance(app, FastAPI)

#     # Get all routes in the app
#     routes = [route.path for route in app.routes]

#     # Assert that the expected endpoints are registered
#     assert len(list(filter(lambda x: x.startswith("/api/v1/health/"), routes))) > 0
#     assert len(list(filter(lambda x: x.startswith("/api/v1/auth/"), routes))) > 0
#     assert len(list(filter(lambda x: x.startswith("/api/v1/protected/"), routes))) > 0
#     # with TestClient(app) as client:
#     #     # Ensure the app includes the mocked routers
#     #     assert client.app.router.routes[0].path == "/api/v1/health"
#     #     assert client.app.router.routes[1].path == "/api/v1/upload"
#     #     assert client.app.router.routes[2].path == "/api/v1/search"
#     #     assert client.app.router.routes[3].path == "/api/v1/rag"

# # # Required to mock create_async_engine
# # @pytest.fixture(autouse=True)
# # def mock_create_async_engine():
# #     with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_async_engine:
# #         yield mock_async_engine

# # @pytest.fixture(autouse=True)
# # def mock_create_engine():
# #     with patch("sqlalchemy.create_engine") as mock_engine:
# #         yield mock_engine

# # @pytest.fixture(autouse=True)
# # def mock_generate_embeddings_task():
# #     with patch("app.tasks.embedding.generate_embeddings_task") as mock_generate_embeddings_task:
# #         yield mock_generate_embeddings_task

# # @pytest.fixture(autouse=True)
# # def mock_llm():
# #     with patch("app.llm") as mock_llm:
# #         mock_llm.openai_client = AsyncMock()
# #         yield mock_llm

# # @pytest.fixture(autouse=True)
# # def mock_create_engine():
# #     with patch("app.llm.openai_client") as mock_open_api_client:
# #         yield mock_open_api_client

# # @patch("app.main.sync_engine")
# # @patch("app.main.async_engine")
# # @patch("app.main.Base")
# # def test_lifespan(mock_base, mock_async_engine, mock_sync_engine):
# #     from app.main import app
# #     mock_async_engine.begin.return_value.__aenter__.return_value.run_sync = AsyncMock()

# #     # Test the lifespan function indirectly by starting the app
# #     with TestClient(app) as client:
# #         pass  # The lifespan is triggered when the TestClient is used

# #     mock_async_engine.begin.assert_called_once()
# #     mock_async_engine.begin.return_value.__aenter__.return_value.run_sync.assert_called_once_with(mock_base.metadata.create_all)

# # # Mock the routers
# # @patch("app.main.health.router")
# # @patch("app.main.upload.router")
# # @patch("app.main.search.router")
# # @patch("app.main.rag.router")
# # def test_routes(mock_rag_router, mock_search_router, mock_upload_router, mock_health_router):
# #     from app.main import app
# #     with TestClient(app) as client:
# #         # Ensure the app includes the mocked routers
# #         assert client.app.router.routes[0].path == "/api/v1/health"
# #         assert client.app.router.routes[1].path == "/api/v1/upload"
# #         assert client.app.router.routes[2].path == "/api/v1/search"
# #         assert client.app.router.routes[3].path == "/api/v1/rag"