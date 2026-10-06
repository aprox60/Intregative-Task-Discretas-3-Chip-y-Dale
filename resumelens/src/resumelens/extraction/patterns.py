from __future__ import annotations

import re


def build_pattern_catalog() -> dict[str, re.Pattern[str]]:
    """Build a dictionary of regular-expression patterns for relevant résumé features.

    These patterns are intentionally lightweight and local. They capture explicit textual
    evidence but do not decide whether a candidate matches a profile.
    """

    return {
        "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
        "phone": re.compile(
            r"(?i)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)\d{3}[-.\s]?\d{4}"
        ),
        "url": re.compile(r"(?i)https?://\S+|www\.\S+"),
        "programming_language": re.compile(
            r"(?i)\b(python|javascript|js|java|c\+\+|c#|ruby|php|go|rust|swift|typescript)\b"
        ),
        "framework": re.compile(
            r"(?i)\b(react|react\.js|node\.js|nodejs|django|spring\s*boot|flask|angular|vue|pandas|scikit\-learn|tensorflow|pytorch)\b"
        ),
        "database": re.compile(r"(?i)\b(postgres|postgresql|mysql|mongodb|sqlite|redis|sql)\b"),
        "tool": re.compile(r"(?i)\b(git|docker|kubernetes|linux|aws|azure|jenkins|figma)\b"),
        "academic_qualification": re.compile(
            r"(?i)\b(bsc|bs|ba|msc|m\.sc|phd|master\s*degree|bachelor\s*degree)\b"
        ),
        "experience": re.compile(
            r"(?i)(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of\s+)?experience"
        ),
    }


def extract_by_category(text: str, category: str) -> list[str]:
    """Return all matches for a specific extraction category."""

    catalog = build_pattern_catalog()
    pattern = catalog.get(category)
    if pattern is None:
        raise ValueError(f"Unknown extraction category: {category}")
    return [match.group(0).strip() for match in pattern.finditer(text)]


def extract_contact_info(text: str) -> dict[str, list[str]]:
    """Extract contact information and return the raw values as a dictionary."""

    return {
        "email": extract_by_category(text, "email"),
        "phone": extract_by_category(text, "phone"),
        "links": extract_by_category(text, "url"),
    }


def extract_programming_languages(text: str) -> list[str]:
    """Extract programming languages using the programming-language regex."""

    return extract_by_category(text, "programming_language")


def extract_frameworks(text: str) -> list[str]:
    """Extract frameworks, libraries, and platforms from the raw text."""

    return extract_by_category(text, "framework")


def extract_databases(text: str) -> list[str]:
    """Extract database technology names."""

    return extract_by_category(text, "database")


def extract_tools(text: str) -> list[str]:
    """Extract tools and technologies."""

    return extract_by_category(text, "tool")


def extract_academic_qualifications(text: str) -> list[str]:
    """Extract education and academic qualification evidence."""

    return extract_by_category(text, "academic_qualification")


def extract_experience(text: str) -> list[str]:
    """Extract experience evidence such as '3 years of experience'."""

    return extract_by_category(text, "experience")


def extract_generic_skills(text: str) -> list[str]:
    """Collect all generic skill evidence into one list.

    This function is intentionally broad and does not decide whether the skill is relevant
    to a specific profile. The formal profile pattern is decided later in the pipeline.
    """

    variant_patterns = re.compile(
        r"(?i)\b(?:react(?:[\s.-]?js)?|node(?:[\s.-]?js)?|nodejs|postgres(?:ql)?|javascript|js|git|python|pandas|scikit(?:[\s-]?learn)|tensorflow|pytorch|sql|numpy)\b"
    )
    matches = [match.group(0).strip() for match in variant_patterns.finditer(text)]
    return [match for index, match in enumerate(matches) if match and match not in matches[:index]]


def extract_candidate_evidence(text: str) -> dict[str, list[str]]:
    """Return a dictionary of extracted evidence grouped by category."""

    contact = extract_contact_info(text)
    return {
        "contact": [
            *contact["email"],
            *contact["phone"],
            *contact["links"],
        ],
        "email": contact["email"],
        "phone": contact["phone"],
        "links": contact["links"],
        "programming_languages": extract_programming_languages(text),
        "frameworks": extract_frameworks(text),
        "databases": extract_databases(text),
        "tools": extract_tools(text),
        "academic_qualifications": extract_academic_qualifications(text),
        "experience": extract_experience(text),
        "skills": extract_generic_skills(text),
    }
