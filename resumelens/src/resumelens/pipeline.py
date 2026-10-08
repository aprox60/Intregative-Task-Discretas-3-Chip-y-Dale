from resumelens.classification.classifier import classify_all_profiles
from resumelens.dsl.generator import candidate_to_dsl
from resumelens.dsl.visualizer import render_html
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.models import Candidate, PipelineResult
from resumelens.normalization.lexicon import normalize_tokens
from resumelens.normalization.sorter import sort_candidates


def run_resume_pipeline(raw_text, profile_name=None):
    # Runs all the stages over the text of one resume
    extracted = ResumeExtractor(raw_text).extract()
    normalized = normalize_tokens(extracted.get_all_technical_strings())
    ordered = sort_candidates(normalized, profile_name)
    classification = classify_all_profiles(ordered)

    name = extracted.name
    if name == "":
        name = "Candidate"
    email = "example@example.com"
    if len(extracted.emails) > 0:
        email = extracted.emails[0]
    phone = "+0000000000"
    if len(extracted.phones) > 0:
        phone = extracted.phones[0]

    qualifications = []
    for entry in extracted.education:
        qualifications.append(entry.degree + " in " + entry.field)
    experience = []
    for entry in extracted.experience:
        experience.append(str(entry.years) + " years - " + entry.description)

    candidate = Candidate(name, email, phone, extracted.links, ordered, qualifications, experience, classification)

    dsl_text = candidate_to_dsl(candidate)
    html = render_html(candidate)
    return PipelineResult(candidate, extracted, ordered, classification, dsl_text, html)
