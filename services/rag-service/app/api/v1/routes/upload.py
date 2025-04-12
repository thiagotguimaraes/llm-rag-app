from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.tasks.embedding import generate_embeddings_task

router = APIRouter()

class DocumentRequest(BaseModel):
    texts: List[str]

class TaskResponse(BaseModel):
    task_id: str

@router.post("/ingest", response_model=TaskResponse)
async def ingest_documents(payload: DocumentRequest):
    task = generate_embeddings_task.delay(payload.texts)
    return TaskResponse(task_id=task.id)