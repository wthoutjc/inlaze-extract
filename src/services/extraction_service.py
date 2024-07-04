from fastapi import HTTPException
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
        channel.exchange_declare(exchange='extraction', exchange_type='direct')
        channel.queue_declare(queue='extraction_queue')

        channel.basic_publish(
            exchange='extraction',
            routing_key='extraction.queue',
            body=json.dumps(message)
        )
        connection.close()

    def start_extraction(self, job_data: ExtractionJobCreate) -> ExtractionJobStatus:
        job = ExtractionJob(
            endpoint_url=str(job_data.endpoint_url),
            status=JobStatus.IN_PROGRESS
        )
        self.repository.add(job)

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

    def get_extraction_status(self, job_id: int) -> ExtractionJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return ExtractionJobStatus(id=job.id, status=job.status)