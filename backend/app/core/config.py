from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""

    database_url: str = "postgresql://user:password@localhost:5432/dollarresume"

    supabase_url: str = ""
    supabase_anon_key: str = ""

    billing_enabled: bool = False
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_publishable_key: str = ""

    app_base_url: str = "http://localhost:8000"
    session_secret: str = "change-me-to-a-long-random-string"


@lru_cache
def get_settings() -> Settings:
    return Settings()
