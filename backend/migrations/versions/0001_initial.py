"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-20

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "resumes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False, server_default="Untitled resume"),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_resumes_user_id", "resumes", ["user_id"])

    op.create_table(
        "credits_ledger",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("delta", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=200), nullable=False),
        sa.Column("stripe_session_id", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_credits_ledger_user_id", "credits_ledger", ["user_id"])
    op.create_index(
        "ix_credits_ledger_stripe_session_id", "credits_ledger", ["stripe_session_id"]
    )

    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stripe_session_id", sa.String(length=200), nullable=False, unique=True),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_payments_user_id", "payments", ["user_id"])


def downgrade() -> None:
    op.drop_table("payments")
    op.drop_table("credits_ledger")
    op.drop_table("resumes")
