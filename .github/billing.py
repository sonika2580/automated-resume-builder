"""
Stripe checkout + webhook. Only relevant when BILLING_ENABLED=true — self-hosted instances
with billing off should never hit these in normal use. Real implementation lands in
Milestone 4.
"""

from fastapi import APIRouter, HTTPException, Request, status

from app.config import get_settings

router = APIRouter()


@router.post("/checkout")
async def create_checkout_session():
    """Create a $1 Stripe Checkout Session for a generate/save/update action."""
    settings = get_settings()
    if not settings.billing_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Billing is disabled on this instance")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 4")


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Verify the Stripe signature and credit one action on checkout.session.completed.
    Must be idempotent — Stripe retries deliveries, so duplicate events must not double-credit.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 4")
