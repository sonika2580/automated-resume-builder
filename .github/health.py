from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check():
    """Liveness check. Also surfaces whether billing is on, which is handy when debugging
    why a self-hosted instance is (or isn't) asking for payment."""
    settings = get_settings()
    return {
        "status": "ok",
        "billing_enabled": settings.billing_enabled,
    }
