"""
Save/load/update resumes for a signed-in user.

Stubbed out for now — real implementation lands in Milestone 6, once Milestone 2
(database & accounts) provides get_current_user and a db session.
"""

from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("")
def list_resumes():
    """List saved resumes for the current user."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 6")


@router.post("")
def create_resume():
    """Save a new resume version. Consumes one credit once billing is enabled."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 6")


@router.get("/{resume_id}")
def get_resume(resume_id: str):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 6")


@router.put("/{resume_id}")
def update_resume(resume_id: str):
    """Update a saved resume. Consumes one credit once billing is enabled."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 6")
