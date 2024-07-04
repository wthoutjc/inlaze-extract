from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.extraction_job import ExtractionJob, JobStatus
from src.repositories.extraction_job_repository import ExtractionJobRepository
from src.schemas.extraction_job import ExtractionJobCreate, ExtractionJobStatus
import requests
import pika
import json

class ExtractionService:
    def __init__(self, repository: ExtractionJobRepository):
        self.repository = repository

    def _send_to_queue(self, message: dict):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='extraction_queue')

        channel.basic_publish(
            exchange='',
            routing_key='extraction_queue',
            body=json.dumps(message)
        )
        connection.close()

    def start_extraction(self, job_data: ExtractionJobCreate, db: Session) -> ExtractionJobStatus:
        job = ExtractionJob(
            source_db=job_data.source_db,
            query=job_data.query,
            status=JobStatus.IN_PROGRESS
        )
        job = self.repository.add(job)

        try:
            response = requests.get(job.endpoint_url)
            response.raise_for_status()
            job.status = JobStatus.COMPLETED

            self._send_to_queue({
                'job_id': job.id,
                'data': response.json()
            })
        except requests.RequestException:
            job.status = JobStatus.FAILED

        self.repository.update(job)
        return ExtractionJobStatus(id=job.id, status=job.status)

    def get_extraction_status(self, job_id: int, db: Session) -> ExtractionJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return ExtractionJobStatus(id=job.id, status=job.status)