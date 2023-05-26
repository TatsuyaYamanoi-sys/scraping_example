import os

from pydantic import BaseModel


class EnvModel(BaseModel):
    JWT_SECRET_KEY: str
    
    SELENIUM_URL: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DIALECT: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    BASIC_USER: str
    BASIC_PASSWORD: str

    LANCERS_USERNAME: str
    LANCERS_PASSWORD: str

    TZ: str


env = EnvModel(**os.environ)
