"""
Shared FastAPI dependencies.
"""

import httpx
from fastapi import Header, HTTPException, status

from app.config import get_settings


async def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    """
    Verifies the bearer token against Supabase's Auth API and returns {id, email}.

    This calls Supabase on every request rather than verifying the JWT locally — slightly
    more latency, but it means a revoked/expired session is rejected immediately without us
    having to manage JWT secrets or rotation ourselves. Fine for this app's request volume;
    revisit with local JWT verification + caching if it ever becomes a bottleneck.
    """
    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not settings.supabase_url or not settings.supabase_anon_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Supabase isn't configured"
        )

    token = authorization.split(" ", 1)[1]
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={"apikey": settings.supabase_anon_key, "Authorization": f"Bearer {token}"},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    data = resp.json()
    return {"id": data["id"], "email": data.get("email")}

