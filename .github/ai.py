"""
The two AI-backed features from the frontend: importing an existing resume file, and the
resume checker with approvable suggested edits. Both currently run through the browser's
Claude artifact capabilities; this is where that logic moves server-side so the app works
outside claude.ai. Real implementation lands in Milestone 3.
"""

from fastapi import APIRouter, HTTPException, UploadFile, status

router = APIRouter()


@router.post("/import")
async def import_resume(file: UploadFile):
    """
    Extract text from an uploaded PDF/DOCX/TXT resume (pdfplumber / python-docx server-side,
    replacing the pdf.js/mammoth.js used in the browser prototype) and ask the Anthropic API
    to structure it into the resume JSON schema the frontend expects.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 3")


@router.post("/check")
async def check_resume():
    """
    Take the current resume JSON from the frontend, ask the Anthropic API for a recruiter-style
    review, and return score/strengths/improvements plus suggested_summary, suggested_experience,
    and suggested_skills_add — same shape the frontend's checker UI already renders.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Milestone 3")
