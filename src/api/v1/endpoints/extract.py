from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.extraction_job import ExtractionJobCreate, ExtractionJobStatus
from src.services.extraction_service import ExtractionService
from src.repositories.extraction_job_repository import ExtractionJobRepository
from src.database.session import get_db

router = APIRouter()

def get_extraction_service(db: Session = Depends(get_db)) -> ExtractionService:
    repository = ExtractionJobRepository(db)
    return ExtractionService(repository)

@router.post("/extract", response_model=ExtractionJobStatus)
def start_extraction(
    job: ExtractionJobCreate,
    db: Session = Depends(get_db),
    extraction_service: 'ExtractionService' = Depends(get_extraction_service)
):
    return extraction_service.start_extraction(job, db)

@router.get("/extract/status/{job_id}", response_model=ExtractionJobStatus)
def get_extraction_status(
    job_id: int,
    db: Session = Depends(get_db),
    extraction_service: 'ExtractionService' = Depends(get_extraction_service)
):
    return extraction_service.get_extraction_status(job_id, db)
