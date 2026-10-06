from __future__ import annotations

import re

from resumelens.dsl.parser import ResumeParser


class ResumeValidationError(ValueError):
    """Raised when a candidate DSL document violates the formal language constraints."""


def validate_resume_dsl(text: str) -> object:
    """Parse a resume DSL document and reject invalid syntax or lexical values."""

    parser = ResumeParser()
    model = parser.parse_text(text)
    if not getattr(model, "candidate", None):
        raise ResumeValidationError("Missing candidate information in the DSL model.")

    email = getattr(getattr(model, "contact", {}), "get", lambda *_: None)("email") if hasattr(model, "contact") and isinstance(model.contact, dict) else None
    if not email:
        raise ResumeValidationError("Missing contact email in the DSL model.")
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(email)):
        raise ResumeValidationError(f"Invalid email lexical form: {email}")

    phone = getattr(getattr(model, "contact", {}), "get", lambda *_: None)("phone") if hasattr(model, "contact") and isinstance(model.contact, dict) else None
    if phone and not re.fullmatch(r"\+?[0-9()\-\s]{7,}", str(phone)):
        raise ResumeValidationError(f"Invalid phone lexical form: {phone}")

    profile = getattr(model, "classification", None)
    if profile is not None:
        status = profile.get("status") if isinstance(profile, dict) else None
        if status not in {"ACCEPTED", "REJECTED"}:
            raise ResumeValidationError(f"Invalid classification status: {status}")

    return model


def validate_resume_text(text: str) -> object:
    """Compatibility wrapper for validation entry points."""

    return validate_resume_dsl(text)
