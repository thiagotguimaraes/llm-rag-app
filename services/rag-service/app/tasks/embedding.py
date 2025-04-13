import asyncio
from app.worker import celery_app
from app.services.embedding import EmbeddingService
from app.qdrant_client import store_embeddings
from app.services.chunking import chunk_text
from app.db.session import get_async_session
from app.db.models import Document, DocumentStatus
from app.db.session import async_session

embedder = EmbeddingService()

@celery_app.task
def generate_embeddings_task(texts: list[str], user_id: str) -> str:
    vectors = embedder.embed(texts)
    store_embeddings(vectors, texts, user_id)
    return f"{len(texts)} documents stored for user {user_id}."


@celery_app.task
def process_document(document_id: str, filename: str, content: str, user_id: str):
    try:
        loop = asyncio.get_event_loop()  # Try to get the current event loop
    except RuntimeError:  # No event loop exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(_process_document_async(document_id, filename, content, user_id))
    
async def _process_document_async(document_id: str, filename: str, content: str, user_id: str):
    async with async_session() as session:  # Use async session properly
        doc = await session.get(Document, document_id)  # Use `await` for async queries
        if not doc:
            return

        try:
            doc.status = DocumentStatus.processing
            await session.commit()

            chunks = chunk_text(content)
            vectors = embedder.embed(chunks)
            store_embeddings(vectors, chunks, user_id)

            doc.status = DocumentStatus.done
            await session.commit()
        except Exception as e:
            doc.status = DocumentStatus.failed
            await session.commit()
            raise e