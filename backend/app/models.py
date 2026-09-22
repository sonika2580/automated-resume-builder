"""
App-owned tables. user_id columns reference Supabase's auth.users.id but aren't enforced
as a cross-schema foreign key — that keeps our Alembic migrations independent of whatever
Supabase manages internally in the `auth` schema.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), default="Untitled resume")
    data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CreditLedgerEntry(Base):
    """Append-only ledger. Balance = sum(delta) for a user. +1 on a paid credit, -1 on a
    consumed action. Never update or delete a row — that's what makes double-spend and
    double-credit bugs easy to audit."""

    __tablename__ = "credits_ledger"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    stripe_session_id: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    """One row per Stripe Checkout Session. stripe_session_id is unique so the webhook
    can be replayed safely without creating duplicate payment records."""

    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    stripe_session_id: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
