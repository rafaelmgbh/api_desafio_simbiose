from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = 'api/v1'
    DB_URL: str = 'postgresql+asyncpg://admin:admin@localhost:5432/fastapi'
    DBBAseModel = declarative_base()

    JWT_SECRET: str = 'Ud7oha7t8DiDQRwKc0bNT8gOeQtcecSoa0uf2jDjKLE'
    JWT_REFRESH_SECRET_KEY: str = 'teste do teste'
    """
    import secrets 
    token : str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        case_sensitive: True


settings: Settings = Settings()
