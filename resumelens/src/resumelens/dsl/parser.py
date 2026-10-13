# Stage 4: parses and validates candidate profiles written in the ResumeLens DSL.
#
# There are three kinds of errors:
# - lexical: a value does not match its terminal, for example an email without "@"
# - syntactic: the structure is wrong, for example a missing "{" or a missing email
# - semantic: the structure is right but the content makes no sense, for example
#   the same profile evaluated twice or 80 years of experience
# textX finds the first two kinds. The third kind is checked with object processors.

import os

from textx import TextXSemanticError, TextXSyntaxError, get_location, metamodel_from_file

GRAMMAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resume.tx")

MAX_YEARS = 60


class ResumeValidationError(Exception):

    def __init__(self, kind, message, line=None, column=None):
        self.kind = kind
        self.message = message
        self.line = line
        self.column = column
        text = kind + " error: " + message
        if line is not None:
            text = text + " (line " + str(line) + ", column " + str(column) + ")"
        Exception.__init__(self, text)


def semantic_error(message, obj):
    location = get_location(obj)
    raise TextXSemanticError(message, line=location["line"], col=location["col"])


def check_candidate(candidate):
    if candidate.name.strip() == "":
        semantic_error("the candidate name can't be empty", candidate)


def check_experience(experience):
    if experience.years > MAX_YEARS:
        semantic_error("years of experience must be at most " + str(MAX_YEARS), experience)


def check_skills(skills):
    seen = []
    for token in skills.tokens:
        if token in seen:
            semantic_error("skill " + token + " is repeated", skills)
        seen.append(token)


def check_evaluation(evaluation):
    seen = []
    for result in evaluation.results:
        if result.profile in seen:
            semantic_error("profile " + result.profile + " is evaluated more than once", result)
        seen.append(result.profile)


def build_metamodel():
    metamodel = metamodel_from_file(GRAMMAR_PATH)
    metamodel.register_obj_processors({
        "CandidateProfile": check_candidate,
        "Experience": check_experience,
        "Skills": check_skills,
        "Evaluation": check_evaluation,
    })
    return metamodel


METAMODEL = build_metamodel()


# Terminals defined by regular expressions. When textX expected one of them and the text
# did not match, the problem is in a value (lexical) and not in the structure (syntactic)
LEXICAL_TERMINALS = ["Email", "Phone", "Url", "Token", "INT", "STRING"]


def error_kind(message):
    expected = message.split("Expected ")
    if len(expected) > 1:
        for terminal in LEXICAL_TERMINALS:
            if expected[1].startswith(terminal):
                return "Lexical"
    return "Syntax"


def parse_dsl(text):
    # Returns the textX model, or raises ResumeValidationError explaining what is wrong
    try:
        return METAMODEL.model_from_str(text)
    except TextXSyntaxError as error:
        message = str(error.message)
        raise ResumeValidationError(error_kind(message), message, error.line, error.col)
    except TextXSemanticError as error:
        raise ResumeValidationError("Semantic", str(error.message), error.line, error.col)


def is_valid(text):
    try:
        parse_dsl(text)
        return True
    except ResumeValidationError:
        return False
