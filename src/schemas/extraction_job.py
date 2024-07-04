from pydantic import BaseModel
from enum import Enum

class JobStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionJobCreate(BaseModel):
    source_db: str
    query: str

class ExtractionJobStatus(BaseModel):
    id: int
    status: JobStatusEnum
