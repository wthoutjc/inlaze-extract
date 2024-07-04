from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.extraction_job import ExtractionJob, JobStatus
from src.repositories.extraction_job_repository import ExtractionJobRepository
from src.schemas.extraction_job import ExtractionJobCreate, ExtractionJobStatus

class ExtractionService:
    def __init__(self, repository: ExtractionJobRepository):
        self.repository = repository

    def start_extraction(self, job_data: ExtractionJobCreate, db: Session) -> ExtractionJobStatus:
        job = ExtractionJob(
            source_db=job_data.source_db,
            query=job_data.query,
            status=JobStatus.IN_PROGRESS
        )
        job = self.repository.add(job)

        # Lógica para ejecutar la extracción de datos aquí

        job.status = JobStatus.COMPLETED  # o JobStatus.FAILED si ocurre un error
        self.repository.update(job)
        return ExtractionJobStatus(id=job.id, status=job.status)

    def get_extraction_status(self, job_id: int, db: Session) -> ExtractionJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return ExtractionJobStatus(id=job.id, status=job.status)