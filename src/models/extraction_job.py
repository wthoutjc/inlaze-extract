from sqlalchemy import Column, String, Enum
from enum import Enum as PyEnum
import uuid
from src.database.base import Base

class JobStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionJob(Base):
    __tablename__ = "extraction_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint_url = Column(String, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)