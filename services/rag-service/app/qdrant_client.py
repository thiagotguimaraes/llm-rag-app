import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
import os
load_dotenv()

logger = logging.getLogger(__name__)

QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

qdrant = QdrantClient(host="qdrant", port=QDRANT_PORT)

def init_qdrant():
    logger.info("🚀 Initializing Qdrant client...")
    collection_name = "test-collection"
    if collection_name not in qdrant.get_collections().collections:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3, distance=Distance.COSINE),
        )
    logger.info("✅ Qdrant is ready")
