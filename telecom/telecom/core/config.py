from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_v1_str: str = "/api/v1"
    app_title: str = "Телеком услуги"
    model_config = SettingsConfigDict(
        env_prefix="telecom_",
        env_file=("ENV/.env", "ENV/.env.prod"),
        env_file_encoding="utf-8",
        validate_default=False,
    )


settings = Settings()
