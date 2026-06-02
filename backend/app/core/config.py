from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Medical Recommendations API"
    postgres_user: str = "medical_user"
    postgres_password: str = "medical_password"
    postgres_db: str = "medical_recommendations"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: str | None = None
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    redis_url: str | None = None
    public_questions_cache_ttl_seconds: int = 600
    first_admin_email: str = "admin@example.com"
    first_admin_password: str = "admin12345"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @computed_field
    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            "postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
