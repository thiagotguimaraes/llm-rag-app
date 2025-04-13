from fastapi import Query
from app.qdrant_client import qdrant
from app.services.embedding import embedding_service
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def search_documents(query: str = Query(...)):
    vector = embedding_service.embed([query])
    
    result = qdrant.search(
        collection_name="test-collection",
        query_vector=vector,
        limit=5,
        with_payload=True,
    )
    print('result', result)
    return [
        {"text": hit.payload["text"], "score": hit.score}
        for hit in result
    ]
