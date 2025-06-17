from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

env_file_path = Path.cwd() / ".env"


class Settings(BaseSettings):
    mongodb_url: str
    admin_token: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=env_file_path, case_sensitive=False)


settings = Settings()
