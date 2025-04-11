from fastapi import APIRouter, status
from pydantic import BaseModel
from app.tasks.embed import embed_and_store_document

router = APIRouter()

class DocumentInput(BaseModel):
    text: str

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_document(doc: DocumentInput):
    task = embed_and_store_document.delay(doc.text)
    return {"task_id": task.id}