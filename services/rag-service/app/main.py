from fastapi import FastAPI
from app.qdrant_client import init_qdrant
from app.api.v1.routes import upload, health

async def lifespan(app: FastAPI):
    init_qdrant()
    yield

app = FastAPI(title="RAG Microservice", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1/health")
app.include_router(upload.router, prefix="/api/v1/upload")
