from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str

    AUTH_SERVICE_URL: str
    USER_SERVICE_URL: str
    TASK_SERVICE_URL: str

    class Config:
        env_file = BASE_DIR / ".env"

settings = Settings()