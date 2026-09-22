from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.services.credits import get_credit_balance

router = APIRouter()


@router.get("/me")
def get_me(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Who's signed in, and how many credits they have left. The frontend uses this to
    show/hide the '$1 to continue' prompt."""
    balance = get_credit_balance(db, user["id"])
    return {"id": user["id"], "email": user["email"], "credits": balance}
