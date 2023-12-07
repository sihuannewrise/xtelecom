from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Телеком услуги"
    pg_dsn: PostgresDsn = "postgres://user:pass@localhost:5432/telecom"
    model_config = SettingsConfigDict(
        env_prefix="telecom_",
        env_file=("ENV/.env", "ENV/.env.prod"),
        env_file_encoding="utf-8",
    )


settings = Settings()
