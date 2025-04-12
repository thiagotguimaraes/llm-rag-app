from app.worker import celery_app
from app.embedding.service import EmbeddingService
from app.qdrant_client import store_embeddings

embedder = EmbeddingService()

@celery_app.task
def generate_embeddings_task(texts: list[str], user_id: str) -> str:
    vectors = embedder.embed(texts)
    collection_name = f"user_{user_id}_documents"
    store_embeddings(vectors, texts, collection_name)
    return f"{len(texts)} documents stored for user {user_id}."
