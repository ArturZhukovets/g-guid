import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = os.path.join(BASE_DIR, ".env")
# print(env_path)
# load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, case_sensitive=False)  # TODO handle how to work with this field
    PROJECT_NAME: str = "G-Guid"
    PROJECT_VERSION: str = "0.1.0"

    # DB
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field()
    DB_ECHO: bool = False

    @property
    def database_url(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    ENCODE_ALGORITHM: str = "HS256"
    SECRET_KEY: str = Field()

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

    # Translation
    LINGVANEX_API_URL: str
    LINGVANEX_API_KEY: str


settings = Settings()
