from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.tasks.embedding import generate_embeddings_task
from app.api.auth import get_current_user_id

router = APIRouter()

class DocumentRequest(BaseModel):
    texts: List[str]

class TaskResponse(BaseModel):
    task_id: str

@router.post("/ingest", response_model=TaskResponse)
async def ingest_documents(payload: DocumentRequest, user_id: str = Depends(get_current_user_id)):
    task = generate_embeddings_task.delay(payload.texts, user_id)
    return TaskResponse(task_id=task.id)