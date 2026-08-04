from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "CodeGuardian AI"
    app_env: str = Field(default="development", alias="APP_ENV")
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173"]

    database_url: str = Field(
        default="postgresql+psycopg://codeguardian:codeguardian@localhost:5432/codeguardian",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    jwt_secret_key: str = Field(default="change-me-in-production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    github_client_id: str | None = Field(default=None, alias="GITHUB_CLIENT_ID")
    github_client_secret: str | None = Field(default=None, alias="GITHUB_CLIENT_SECRET")
    github_app_id: str | None = Field(default=None, alias="GITHUB_APP_ID")
    github_app_private_key: str | None = Field(default=None, alias="GITHUB_APP_PRIVATE_KEY")
    github_webhook_secret: str | None = Field(default=None, alias="GITHUB_WEBHOOK_SECRET")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    rag_index_path: str = Field(default="backend/data/faiss.index", alias="RAG_INDEX_PATH")
    standards_corpus_path: str = Field(default="backend/data/standards", alias="STANDARDS_CORPUS_PATH")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
