from resumelens.classification.classifier import classify
from resumelens.classification.profiles import PROFILES
from resumelens.dsl.generator import candidate_to_dsl
from resumelens.dsl.visualizer import render_html
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.models import Candidate, PipelineResult
from resumelens.normalization.normalizer import normalize_extraction
from resumelens.normalization.sorter import sort_for_all_profiles


def run_resume_pipeline(raw_text):
    # Stage 1: regular expressions
    extracted = ResumeExtractor(raw_text).extract()

    # Stage 2: transducers and canonical order of each profile
    normalization = normalize_extraction(extracted)
    sorted_by_profile = sort_for_all_profiles(normalization.tokens, PROFILES)

    # Stage 3: each profile automaton reads its own sorted sequence
    classification = {}
    for profile_name in PROFILES:
        classification[profile_name] = classify(sorted_by_profile[profile_name], profile_name)

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

    candidate = Candidate(name, email, phone, extracted.links, normalization.tokens, qualifications, experience, classification)

    # Stage 4: DSL and visualization
    dsl_text = candidate_to_dsl(candidate)
    html = render_html(candidate)

    result = PipelineResult(candidate, extracted, normalization.tokens, classification, dsl_text, html)
    result.normalization = normalization
    result.sorted_by_profile = sorted_by_profile
    return result
