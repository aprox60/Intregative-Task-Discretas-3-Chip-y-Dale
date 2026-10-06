"""Extraction stage package."""

from resumelens.extraction.extractor import ResumeExtractor, extract_resume
from resumelens.extraction.patterns import (
    build_pattern_catalog,
    extract_academic_qualifications,
    extract_candidate_evidence,
    extract_contact_info,
    extract_databases,
    extract_experience,
    extract_frameworks,
    extract_generic_skills,
    extract_programming_languages,
    extract_tools,
)

__all__ = [
    "ResumeExtractor",
    "extract_resume",
    "build_pattern_catalog",
    "extract_academic_qualifications",
    "extract_candidate_evidence",
    "extract_contact_info",
    "extract_databases",
    "extract_experience",
    "extract_frameworks",
    "extract_generic_skills",
    "extract_programming_languages",
    "extract_tools",
]
