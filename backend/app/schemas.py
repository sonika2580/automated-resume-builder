"""
Mirrors the JSON shape the frontend's `state` object already uses, so responses from
/api/import can be handed straight back to the frontend, and requests to /api/check can
be the frontend's state object unchanged.
"""

from pydantic import BaseModel, Field


class LinkItem(BaseModel):
    label: str = ""
    url: str = ""


class ExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    location: str = ""
    start: str = ""
    end: str = ""
    current: bool = False
    bullets: str = ""


class EducationItem(BaseModel):
    school: str = ""
    degree: str = ""
    location: str = ""
    start: str = ""
    end: str = ""
    details: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    link: str = ""


class CertificationItem(BaseModel):
    name: str = ""
    issuer: str = ""
    year: str = ""


class ResumeData(BaseModel):
    name: str = ""
    role: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    links: list[LinkItem] = Field(default_factory=list)
    summary: str = ""
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    certifications: list[CertificationItem] = Field(default_factory=list)
