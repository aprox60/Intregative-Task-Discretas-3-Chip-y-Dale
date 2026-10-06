from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractedItem:
    """A single extracted piece of evidence from the raw résumé text."""

    category: str
    value: str
    source: str = "raw"
    normalized: str | None = None


@dataclass
class Candidate:
    """Structured candidate model used across the pipeline."""

    full_name: str = ""
    email: str = ""
    phone: str = ""
    links: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    academic_qualifications: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    profile_results: dict[str, bool] = field(default_factory=dict)


@dataclass
class ProfileResult:
    """Result object for a specific classification profile."""

    profile_name: str
    accepted: bool
    reasons: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """Result returned by the resume pipeline orchestration."""

    candidate: Candidate
    extracted: dict[str, list[str]]
    normalized_tokens: list[str]
    classification: dict[str, bool]
    dsl_text: str = ""
    html: str = ""
    notes: list[str] = field(default_factory=list)


def make_candidate_from_payload(payload: dict[str, Any]) -> Candidate:
    """Factory for constructing a Candidate from a dictionary payload."""

    return Candidate(
        full_name=str(payload.get("full_name", "")),
        email=str(payload.get("email", "")),
        phone=str(payload.get("phone", "")),
        links=list(payload.get("links", [])),
        skills=list(payload.get("skills", [])),
        academic_qualifications=list(payload.get("academic_qualifications", [])),
        experience=list(payload.get("experience", [])),
        profile_results=dict(payload.get("profile_results", {})),
    )
