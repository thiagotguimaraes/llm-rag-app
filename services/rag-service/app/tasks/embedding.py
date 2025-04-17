import asyncio

from app.db.models import Document, DocumentStatus
from app.db.session import get_sync_session
from app.qdrant_client import store_embeddings
from app.services.chunking_service import chunk_text
from app.services.embedding_service import EmbeddingService
from app.worker import celery_app

embedder = EmbeddingService()


@celery_app.task
def generate_embeddings_task(texts: list[str], user_id: str) -> str:
    vectors = embedder.embed(texts)
    store_embeddings(vectors, texts, user_id)
    return f"{len(texts)} documents stored for user {user_id}."


@celery_app.task
def process_document(document_id: str, filename: str, content: str, user_id: str):
    with get_sync_session() as session:
        doc = session.get(Document, document_id)
        if not doc:
            return

        try:
            doc.status = DocumentStatus.processing
            session.commit()

            chunks = chunk_text(content)
            vectors = embedder.embed(chunks)
            store_embeddings(vectors, chunks, user_id)

            doc.status = DocumentStatus.done
            session.commit()
        except Exception as e:
            doc.status = DocumentStatus.failed
            session.commit()
            raise e
