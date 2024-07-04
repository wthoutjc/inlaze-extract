import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.session import get_db
from src.models.extraction_job import JobStatus
import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_extraction_job(test_db):
    response = client.post(
        "/api/v1/extract",
        json={"source_db": "test_source_db", "query": "SELECT * FROM test_table"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == JobStatus.IN_PROGRESS

def test_get_extraction_status(test_db):
    response = client.post(
        "/api/v1/extract",
        json={"source_db": "test_source_db", "query": "SELECT * FROM test_table"}
    )
    assert response.status_code == 200
    job_id = response.json()["id"]

    response = client.get(f"/api/v1/extract/status/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["status"] in {JobStatus.IN_PROGRESS, JobStatus.COMPLETED, JobStatus.FAILED}