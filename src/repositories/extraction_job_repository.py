from sqlalchemy.orm import Session
from src.models.extraction_job import ExtractionJob

class ExtractionJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, job: ExtractionJob):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: int):
        return self.db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()

    def update(self, job: ExtractionJob):
        self.db.commit()
        self.db.refresh(job)
        return job