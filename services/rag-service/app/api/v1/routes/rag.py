import logging
from typing import List

from app.llm.openai_client import generate_answer
from app.qdrant_client import search_documents
from app.services.auth_service import get_current_user_id
from app.services.embedding_service import embedding_service
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class RetrievedChunk(BaseModel):
    id: str
    score: float
    payload: dict


class AskResponse(BaseModel):
    answer: str
    context: List[RetrievedChunk]


@router.post("/ask", response_model=AskResponse)
async def ask_rag(request: AskRequest, user_id: str = Depends(get_current_user_id)):
    try:
        vectors = embedding_service.embed(request.question)
        chunks = search_documents(vectors, user_id=user_id)
        context_texts = [chunk["payload"]["text"] for chunk in chunks]
        answer = generate_answer(request.question, context_texts)
        return AskResponse(answer=answer, context=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
