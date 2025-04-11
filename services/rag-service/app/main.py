from fastapi import FastAPI
from app.qdrant_client import init_qdrant

async def lifespan(app: FastAPI):
    init_qdrant()

app = FastAPI(title="RAG Microservice", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}
