from sqlalchemy import Column, String, Enum, DateTime
from app.db.base import Base
import enum
import datetime


class DocumentStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    failed = "failed"

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.pending)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)