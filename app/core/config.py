import logging
import os
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки проекта."""

    APP_TITLE: str
    APP_DESCRIPTION: str
    SECRET: str
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "upload")

settings = Settings()
logger = logging.getLogger(__name__)


def configure_logging():
    logging.basicConfig(
        datefmt="%d.%m.%Y %H:%M:%S",
        format="%(asctime)s, %(levelname)s, %(message)s",
        level=logging.INFO
    )
