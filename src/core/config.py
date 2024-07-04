import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://user:password@localhost/dbname")
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()