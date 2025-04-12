# rag_service/app/api/routes/rag.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.qdrant_client import search_documents
from app.api.auth import get_current_user_id
from app.embedding.service import embedding_service

router = APIRouter()

class AskRequest(BaseModel):
    question: str

class RetrievedChunk(BaseModel):
    id: str
    score: float
    payload: dict

@router.post("/ask", response_model=List[RetrievedChunk])
async def ask_rag(request: AskRequest, user_id: str = Depends(get_current_user_id)):
    try:
        vectors = embedding_service.embed(request.question)
        chunks = search_documents(vectors, user_id=user_id)
        return chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
