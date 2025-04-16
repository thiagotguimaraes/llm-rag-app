from fastapi import Query, Depends, APIRouter
from app.api.auth import get_current_user_id
from app.services.embedding import embedding_service
from app.qdrant_client import search_documents
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def search(query: str = Query(...), topk: str = Query(...), user_id: str = Depends(get_current_user_id)):
    vectors = embedding_service.embed(query)
    search_result = search_documents(vectors, user_id=user_id, top_k=int(topk))
    return search_result
