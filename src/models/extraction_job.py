
from sqlalchemy import Column, Integer, String, Enum
from src.database.base import Base
import enum

class JobStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionJob(Base):
    __tablename__ = "extraction_jobs"

    id = Column(Integer, primary_key=True, index=True)
    source_db = Column(String, index=True)
    query = Column(String)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
