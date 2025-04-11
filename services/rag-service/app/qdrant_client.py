from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

qdrant = QdrantClient(host="qdrant", port=6333)  # Docker service name

def init_qdrant():
    collection_name = "test-collection"
    if collection_name not in qdrant.get_collections().collections:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3, distance=Distance.COSINE),
        )
    print("✅ Qdrant is ready")
