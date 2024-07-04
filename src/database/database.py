from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

class Database:
    __instance = None
    _engine = None
    _Session = None

    def __init__(self):
        self._session_instance = None

        ''' Virtually private constructor. '''
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

            self._engine = create_engine(settings.DATABASE_URL)
            self._Session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

            metadata = MetaData()
            metadata.reflect(bind=self._engine)

    @staticmethod
    def get_instance():
        ''' Static access method. '''
        if Database.__instance is None:
            Database()
        return Database.__instance

    def get_db(self) -> Session:
        if not self._session_instance:
            self._session_instance = self._Session()
        return self._session_instance

    def close_db(self):
        if self._session_instance:
            self._session_instance.close()
            self._session_instance = None