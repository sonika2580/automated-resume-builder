"""
Central place for reading configuration from the environment.

Everything here has a safe default for local development except ANTHROPIC_API_KEY
(needed for the import/checker endpoints) and DATABASE_URL (needed once persistence
lands in Milestone 2). BILLING_ENABLED defaults to False so a fresh clone runs fully
open, with no Stripe keys required.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_base_url: str = "http://localhost:8000"
    session_secret: str = "change-me"
    log_level: str = "INFO"

    # AI features
    anthropic_api_key: str = ""

    # Database / auth (Supabase)
    database_url: str = ""
    supabase_url: str = ""
    supabase_anon_key: str = ""

    # Billing — off by default for self-hosted instances
    billing_enabled: bool = False
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_publishable_key: str = ""

    # Frontend origins allowed to call this API
    cors_origins: list[str] = ["http://localhost:5500", "http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
