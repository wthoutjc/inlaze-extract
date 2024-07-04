# uvicorn app:app --host 0.0.0.0 --port 5000 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.extract import router
from src.core.config import settings
import logging
from src.database.base import Base
from src.database.database import Database

database = Database.get_instance()
Base.metadata.create_all(bind=database._engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ETL Extraction Microservice")
app.include_router(router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)