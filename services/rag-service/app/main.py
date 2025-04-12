import logging
from fastapi import FastAPI
from app.qdrant_client import init_qdrant
from app.api.v1.routes import upload, health, search
from dotenv import load_dotenv
import os
load_dotenv()

LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO").upper()

# Configure logging
logging.basicConfig(
    level=LOGGER_LEVEL,  # Set the logging level (can be DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):
    init_qdrant()
    yield
    logger.info("🛑 Application shutdown.")

app = FastAPI(title="RAG Microservice", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1/health")
app.include_router(upload.router, prefix="/api/v1/upload")
app.include_router(search.router, prefix="/api/v1/search")

logger.info("✅ FastAPI application initialized.")
