from typing import List
from uuid import uuid4

from app.db.models import Document, DocumentStatus
from app.db.session import get_async_session
from app.services.auth_service import get_current_user_id
from app.services.pdf import extract_text_from_pdf
from app.tasks.embedding import generate_embeddings_task, process_document
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

router = APIRouter()


class DocumentRequest(BaseModel):
    texts: List[str]


class TaskResponse(BaseModel):
    task_id: str


@router.post("/ingest", response_model=TaskResponse)
async def ingest_documents(
    payload: DocumentRequest, user_id: str = Depends(get_current_user_id)
):
    task = generate_embeddings_task.delay(payload.texts, user_id)
    return TaskResponse(task_id=task.id)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_async_session),
):
    file_bytes = await file.read()

    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file_bytes)
    elif file.filename.endswith(".txt"):
        content = file_bytes.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    doc_id = str(uuid4())
    # Save document entry
    new_doc = Document(
        id=doc_id,
        filename=file.filename,
        user_id=user_id,
        status=DocumentStatus.pending,
    )
    session.add(new_doc)
    await session.commit()

    # ... create document entry, start Celery task
    process_document.delay(doc_id, file.filename, content, user_id)

    return {"message": "File received", "document_id": doc_id}


@router.get("/{document_id}")
async def get_document_status(
    document_id: str, session: Session = Depends(get_async_session)
):
    result = await session.execute(select(Document).where(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document_id": doc.id, "status": doc.status}
