import pytest

from resumelens.dsl.generator import candidate_to_dsl
from resumelens.dsl.parser import ResumeParser
from resumelens.dsl.validator import ResumeValidationError, validate_resume_dsl
from resumelens.models import Candidate


VALID_DSL = '''
candidate "Alice Example"
email alice@example.com
phone +1234567890
links https://example.com
experience "Frontend Engineer" years 3
education "B.S. Computer Science" institution "ICESI"
skill JAVASCRIPT
skill REACT
skill NODE_JS
profile FULL_STACK_DEVELOPER status ACCEPTED
'''

INVALID_LEXICAL_DSL = '''
candidate "Alice"
email invalid-email
profile FULL_STACK_DEVELOPER status ACCEPTED
'''

INVALID_SYNTAX_DSL = '''
candidate "Alice"
email alice@example.com
phone +1234567890
profile FULL_STACK_DEVELOPER ACCEPTED
'''


def test_valid_dsl_parses():
    model = validate_resume_dsl(VALID_DSL)
    assert model is not None


def test_invalid_lexical_dsl_is_rejected():
    with pytest.raises((ValueError, ResumeValidationError)):
        validate_resume_dsl(INVALID_LEXICAL_DSL)


def test_invalid_syntax_dsl_is_rejected():
    with pytest.raises((ValueError, ResumeValidationError)):
        validate_resume_dsl(INVALID_SYNTAX_DSL)


def test_candidate_generator_creates_dsl_output():
    candidate = Candidate(
        full_name="Alice Example",
        email="alice@example.com",
        phone="+1234567890",
        links=["https://example.com"],
        skills=["JAVASCRIPT", "REACT", "NODE_JS"],
        academic_qualifications=["B.S. Computer Science"],
        experience=["Frontend Engineer"],
        profile_results={"FULL_STACK_DEVELOPER": True},
    )
    text = candidate_to_dsl(candidate)
    parser = ResumeParser()
    model = parser.parse_text(text)
    assert model is not None
