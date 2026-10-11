import os

from resumelens.dsl.generator import generate_dsl
from resumelens.dsl.parser import parse_dsl
from resumelens.extraction.extractor import ResumeExtractor
from resumelens.pipeline import run_resume_file, run_resume_pipeline

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_resumes")

VALID_SAMPLES = [
    "wednesday_addams.txt",
    "mary_jane_watson.txt",
    "alex_rivera_backend.txt",
    "nina_patel_data_scientist.txt",
    "kim_possible_multi_profile.txt",
    "invalid_missing_qualification.txt",
]


def sample(filename):
    return os.path.join(SAMPLES, filename)


def test_full_pipeline_with_the_assignment_example():
    result = run_resume_file(sample("wednesday_addams.txt"))
    assert result.extraction.get_all_technical_strings() == ["JS", "React.js", "NodeJS", "Postgres", "Git"]
    assert result.normalization.tokens == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    assert result.sorted_by_profile["FULL_STACK_DEVELOPER"] == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    assert result.get_accepted_profiles() == ["FULL_STACK_DEVELOPER"]
    assert result.error is None
    assert "profile FULL_STACK_DEVELOPER: ACCEPTED" in result.dsl_text
    assert "<h1>Wednesday Addams</h1>" in result.html


def test_every_generated_dsl_is_valid_for_the_grammar():
    for filename in VALID_SAMPLES:
        result = run_resume_file(sample(filename))
        assert result.error is None, filename
        assert result.model.name != ""


def test_model_keeps_the_information_of_the_previous_stages():
    result = run_resume_file(sample("alex_rivera_backend.txt"))
    model = result.model
    assert model.contact.email == "alex.rivera@example.com"
    assert model.contact.phone == "(602) 555-0187"
    assert model.contact.links[0].url == "github.com/arivera"
    assert model.experiences[0].years == 5
    assert model.educations[0].institution == "Universidad Icesi"
    assert "DOCKER" in model.skills.tokens
    statuses = {}
    for profile_result in model.evaluation.results:
        statuses[profile_result.profile] = profile_result.status
    assert statuses["BACKEND_DEVELOPER"] == "ACCEPTED"
    assert statuses["FULL_STACK_DEVELOPER"] == "REJECTED"


def test_resume_without_name_or_email_is_rejected_by_the_grammar():
    result = run_resume_file(sample("invalid_edge_case.txt"))
    assert result.error is not None
    assert result.model is None
    assert result.html == ""


def test_html_shows_every_profile_result():
    result = run_resume_file(sample("kim_possible_multi_profile.txt"))
    assert result.html.count("badge accepted") == 2
    assert result.html.count("badge rejected") == 2
    assert "Full Stack Developer" in result.html


def test_html_escapes_special_characters():
    text = "Ana O'Neil\nEmail: ana@example.com\nSkills: Python, Git\n2 years of experience with <script> tags."
    result = run_resume_pipeline(text)
    assert "<script>" not in result.html
    assert "&lt;script&gt;" in result.html


def test_quotes_inside_values_do_not_break_the_dsl():
    extraction = ResumeExtractor('Ana Lopez\nEmail: ana@example.com\n3 years of experience in "big data".').extract()
    text = generate_dsl(extraction, ["PYTHON"], {"DATA_SCIENTIST": False})
    model = parse_dsl(text)
    assert model.experiences[0].description == "'big data'"
