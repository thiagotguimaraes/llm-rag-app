import logging
import os
import uuid
from typing import List

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

load_dotenv()

logger = logging.getLogger(__name__)

QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

qdrant = QdrantClient(host="qdrant", port=QDRANT_PORT)


def get_collection_name(user_id: str) -> str:
    return f"user-{user_id}-documents"


def create_collection(collection_name: str):
    if collection_name not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def store_embeddings(embeddings: list[list[float]], texts: list[str], user_id: str):
    collection_name = get_collection_name(user_id)
    create_collection(collection_name)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": text},
        )
        for embedding, text in zip(embeddings, texts)
    ]

    qdrant.upsert(collection_name=collection_name, points=points)


def search_documents(
    embedded_question: list[list[float]], user_id: str, top_k: int = 1
) -> List[dict]:
    collection_name = get_collection_name(user_id)

    if collection_name not in [c.name for c in qdrant.get_collections().collections]:
        logger.info(f"Collection {collection_name} does not exist.")
        return []

    search_result = qdrant.search(
        collection_name=collection_name, query_vector=embedded_question, limit=top_k
    )

    return [
        {"id": point.id, "score": point.score, "payload": point.payload}
        for point in search_result
    ]
