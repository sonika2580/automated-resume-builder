import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import CreditLedgerEntry


def get_credit_balance(db: Session, user_id: uuid.UUID | str) -> int:
    result = db.execute(
        select(func.coalesce(func.sum(CreditLedgerEntry.delta), 0)).where(
            CreditLedgerEntry.user_id == user_id
        )
    ).scalar_one()
    return int(result)


def add_credit_entry(
    db: Session,
    user_id: uuid.UUID | str,
    delta: int,
    reason: str,
    stripe_session_id: str | None = None,
) -> CreditLedgerEntry:
    """Record a ledger entry. Positive delta = credit granted, negative = credit spent.
    Caller is responsible for checking balance before spending (see Milestone 4's
    credit-check dependency)."""
    entry = CreditLedgerEntry(
        user_id=user_id, delta=delta, reason=reason, stripe_session_id=stripe_session_id
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
