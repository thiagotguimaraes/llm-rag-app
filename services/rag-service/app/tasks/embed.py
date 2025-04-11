from app.worker import celery_app
from app.qdrant_client import qdrant
from uuid import uuid4
import numpy as np

@celery_app.task
def embed_and_store_document(text: str):
    # 👇 Mock embedding: random 3D vector (replace later with real model)
    vector = np.random.rand(3).tolist()
    
    qdrant.upsert(
        collection_name="test-collection",
        points=[
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": {"text": text},
            }
        ],
    )
    return {"status": "stored", "vector": vector}