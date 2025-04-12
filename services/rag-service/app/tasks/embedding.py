from app.worker import celery_app
from app.embedding.service import EmbeddingService
from app.qdrant_client import store_embeddings

embedder = EmbeddingService()

@celery_app.task
def generate_embeddings_task(texts: list[str], user_id: str) -> str:
    vectors = embedder.embed(texts)
    store_embeddings(vectors, texts, user_id)
    return f"{len(texts)} documents stored for user {user_id}."
