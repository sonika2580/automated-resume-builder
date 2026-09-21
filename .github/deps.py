"""
Shared FastAPI dependencies.

get_current_user is a placeholder until Milestone 2 (database & accounts) wires up real
Supabase JWT verification. Routers that need an authenticated user should depend on it now
so the auth requirement is already in place when the real implementation lands — no router
code will need to change, just this function.
"""

from fastapi import Header, HTTPException, status


async def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    """
    Placeholder auth dependency.

    TODO (Milestone 2): verify the Supabase JWT in the Authorization header and return
    the real user record (id, email, credit balance) instead of raising.
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth isn't wired up yet — see Milestone 2",
    )
