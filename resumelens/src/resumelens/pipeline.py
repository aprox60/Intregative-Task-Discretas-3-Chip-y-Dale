from __future__ import annotations

from resumelens.classification.classifier import classify_all_profiles
from resumelens.dsl.generator import candidate_to_dsl
from resumelens.dsl.visualizer import render_html
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.models import Candidate, PipelineResult
from resumelens.normalization.lexicon import normalize_tokens
from resumelens.normalization.sorter import sort_candidates


def run_resume_pipeline(raw_text: str, profile_name: str | None = None) -> PipelineResult:
    """Run the full ResumeLens pipeline on a raw résumé string.

    The pipeline intentionally uses the generic profile abstraction described in the
    assignment: one pipeline, multiple profile checks, and explicit pattern validation only.
    """

    extracted = ResumeExtractor(raw_text).extract()
    skill_tokens = extracted.get("skills", [])
    normalized = normalize_tokens(skill_tokens)
    ordered = sort_candidates(normalized, profile_name)
    classification = classify_all_profiles(ordered)

    candidate = Candidate(
        full_name="Candidate",
        email=extracted.get("email", ["example@example.com"])[0] if extracted.get("email") else "example@example.com",
        phone=extracted.get("phone", ["+0000000000"])[0] if extracted.get("phone") else "+0000000000",
        links=extracted.get("links", []),
        skills=ordered,
        academic_qualifications=extracted.get("academic_qualifications", []),
        experience=extracted.get("experience", []),
        profile_results=classification,
    )

    dsl_text = candidate_to_dsl(candidate)
    html = render_html(candidate)
    return PipelineResult(
        candidate=candidate,
        extracted=extracted,
        normalized_tokens=ordered,
        classification=classification,
        dsl_text=dsl_text,
        html=html,
        notes=["Pipeline executed successfully.", "Pattern-based classification only."],
    )
