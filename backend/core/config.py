import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = os.path.join(BASE_DIR, ".env")
print(env_path)
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "G-Guid"
    PROJECT_VERSION: str = "0.1.0"

    # DB
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    ENCODE_ALGORITHM: str = "HS256"
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # TESTS
    TEST_USER_NAME: str = "Oleh"
    TEST_USER_PASSWORD: str = "password"
    TEST_ADMIN_NAME: str = "Artur"
    TEST_ADMIN_PASSWORD: str = "password"

    # CORS SETTINGS
    ALLOW_METHODS: list[str] = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
    ALLOW_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_ORIGINS: list[str] = ["*"]


settings = Settings()
