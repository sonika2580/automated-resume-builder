"""
Server-side versions of the two AI features from the frontend prototype: importing an
existing resume file, and the resume checker with approvable suggested edits. Both were
originally implemented via the browser's Claude artifact capabilities (window.claude); this
is the same logic running through the Anthropic API directly, so the app works outside
claude.ai.
"""

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.schemas import ResumeData
from app.services.claude import ask_claude_json
from app.services.extraction import extract_docx_text, extract_pdf_text

router = APIRouter()

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10MB
MAX_EXTRACTED_CHARS = 12000

IMPORT_SCHEMA = """{"name":"","role":"","email":"","phone":"","location":"",
"links":[{"label":"","url":""}],"summary":"",
"experience":[{"company":"","role":"","location":"","start":"YYYY-MM or empty","end":"YYYY-MM or empty","current":false,"bullets":"one highlight per line"}],
"education":[{"school":"","degree":"","location":"","start":"","end":"","details":""}],
"skills":["..."],
"projects":[{"name":"","description":"","link":""}],
"certifications":[{"name":"","issuer":"","year":""}]}"""


@router.post("/import")
async def import_resume(file: UploadFile):
    filename = (file.filename or "").lower()
    if not filename.endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Use a PDF, DOCX, or TXT file"
        )

    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is too large (10MB max)"
        )

    try:
        if filename.endswith(".pdf"):
            text = extract_pdf_text(raw)
        elif filename.endswith(".docx"):
            text = extract_docx_text(raw)
        else:
            text = raw.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Couldn't read that file"
        )

    text = text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No readable text found in that file"
        )

    prompt = (
        "You will receive raw text extracted from someone's existing resume file. "
        "Structure it into JSON matching exactly this schema, using only information present "
        "in the text (leave a field empty rather than inventing anything):\n"
        f"{IMPORT_SCHEMA}\n\n"
        "Respond with ONLY the JSON object, no commentary, no markdown fences.\n\n"
        f"Resume text:\n{text[:MAX_EXTRACTED_CHARS]}"
    )

    try:
        parsed = ask_claude_json(prompt, max_tokens=3000)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="AI parsing failed — try again"
        )

    return parsed


CHECK_SCHEMA = """{"score": <integer 0-100>,
"strengths": ["...", up to 4 short specific strings],
"improvements": ["...", up to 5 short general notes not tied to one rewrite],
"ats_notes": "1-2 sentences on ATS and formatting readiness",
"suggested_summary": "a rewritten, stronger summary if a rewrite genuinely helps, else an empty string",
"suggested_experience": [{"index": <the entry's position below, 0-based>, "bullets": "a rewritten version of that entry's highlights, one per line"}],
"suggested_skills_add": ["skills clearly implied by the experience text but missing from the skills list, at most 5"]}"""


def _resume_to_text(resume: ResumeData) -> str:
    lines = [(resume.name or "Unnamed candidate") + (f" — {resume.role}" if resume.role else "")]
    contact = " | ".join(filter(None, [resume.location, resume.email, resume.phone]))
    if contact:
        lines.append(contact)
    if resume.summary:
        lines.append(f"\nSummary:\n{resume.summary}")
    if resume.experience:
        lines.append("\nExperience (index in brackets — use it to reference this entry):")
        for i, exp in enumerate(resume.experience):
            end = "present" if exp.current else exp.end
            lines.append(f"[{i}] {exp.role} at {exp.company} ({exp.start} to {end})")
            for bullet in filter(None, (exp.bullets or "").split("\n")):
                lines.append(f"    * {bullet}")
    if resume.education:
        lines.append("\nEducation:")
        for edu in resume.education:
            lines.append(f"- {edu.degree}, {edu.school}")
    if resume.skills:
        lines.append(f"\nSkills: {', '.join(resume.skills)}")
    if resume.projects:
        lines.append("\nProjects:")
        for proj in resume.projects:
            lines.append(f"- {proj.name}: {proj.description}")
    return "\n".join(lines)


@router.post("/check")
async def check_resume(resume: ResumeData):
    if not resume.name and not resume.experience:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Add a few details first"
        )

    prompt = (
        "You are an experienced technical recruiter reviewing a resume. Respond with ONLY a "
        "JSON object of this exact shape:\n"
        f"{CHECK_SCHEMA}\n\n"
        "Only propose a rewrite when it is a real improvement — don't touch something already "
        "strong. Base every suggestion strictly on facts already in the resume; never invent "
        "employers, numbers, dates, or accomplishments that aren't there. No markdown fences, "
        "no commentary outside the JSON.\n\n"
        f"Resume:\n{_resume_to_text(resume)}"
    )

    try:
        result = ask_claude_json(prompt, max_tokens=2000)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="AI review failed — try again"
        )

    return result
