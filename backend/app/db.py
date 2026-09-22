"""
SQLAlchemy setup. This connects to the same Postgres database Supabase gives you (the
DATABASE_URL from Project Settings > Database > Connection string) — Supabase owns the
`auth` schema for users and sessions, and our own app tables (resumes, credits_ledger,
payments) live alongside it in the `public` schema, managed by our own Alembic migrations.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True) if settings.database_url else None
SessionLocal = (
    sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine is not None else None
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not set — see .env.example")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
