from resumelens.classification.classifier import classify_all_profiles
from resumelens.classification.profiles import PROFILES
from resumelens.dsl.generator import generate_dsl
from resumelens.dsl.parser import ResumeValidationError, parse_dsl
from resumelens.dsl.visualizer import render_html
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.models import PipelineResult
from resumelens.normalization.normalizer import normalize_extraction
from resumelens.normalization.sorter import sort_for_all_profiles


def run_resume_pipeline(raw_text):
    result = PipelineResult()

    # Stage 1: regular expressions
    result.extraction = ResumeExtractor(raw_text).extract()

    # Stage 2: transducers and canonical order of each profile
    result.normalization = normalize_extraction(result.extraction)
    result.sorted_by_profile = sort_for_all_profiles(result.normalization.tokens, PROFILES)

    # Stage 3: each profile automaton reads its own sorted sequence
    result.classification = classify_all_profiles(result.sorted_by_profile)

    # Stage 4: DSL, validation with the textX grammar and visualization
    result.dsl_text = generate_dsl(result.extraction, result.normalization.tokens, result.classification)
    try:
        result.model = parse_dsl(result.dsl_text)
        result.html = render_html(result.model)
    except ResumeValidationError as error:
        result.error = error
    return result


def run_resume_file(path):
    with open(path, encoding="utf-8") as file:
        return run_resume_pipeline(file.read())
