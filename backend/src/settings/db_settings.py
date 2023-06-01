from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings.env import env


Base = declarative_base()

class BaseEngine(object):
    def __init__(self):
        pg_username=env.POSTGRES_USERNAME
        pg_password=env.POSTGRES_PASSWORD
        pg_db=env.POSTGRES_DB
        pg_dialect=env.POSTGRES_DIALECT
        pg_host=env.POSTGRES_HOST
        pg_port=env.POSTGRES_PORT
        DATABASE_URL=f'{pg_dialect}://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
        self.engine = create_engine(DATABASE_URL, echo=True)

class BaseSession(BaseEngine):
    def __init__(self):
        super().__init__()
        self.__session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=self.engine))

    @property
    def session(self):
        return self.__session