from pydantic import BaseModel, HttpUrl
from enum import Enum

class JobStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionJobCreate(BaseModel):
    endpoint_url: HttpUrl

class ExtractionJobStatus(BaseModel):
    id: str
    status: JobStatusEnum