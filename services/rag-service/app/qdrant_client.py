import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid   
from dotenv import load_dotenv
import os
load_dotenv()

logger = logging.getLogger(__name__)

QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

qdrant = QdrantClient(host="qdrant", port=QDRANT_PORT)    

def create_collection(collection_name: str):
    if collection_name not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
    
def store_embeddings(embeddings: list[list[float]], texts: list[str], collection_name: str):
    create_collection(collection_name)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": text}
        )
        for embedding, text in zip(embeddings, texts)
    ]

    qdrant.upsert(collection_name=collection_name, points=points)
