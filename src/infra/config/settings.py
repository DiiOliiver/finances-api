from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # pragma: no cover
    ENVIRONMENT: str
    DATABASE_URL: str
    DATABASE_NAME: str
    EMAIL_ENABLED: bool
    EMAIL_SENDER: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    EMAIL_LIMIT_PER_HOUR: int
    USER_ID: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
