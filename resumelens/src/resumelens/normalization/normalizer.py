# Stage 2: runs the transducers over the strings found in stage 1

from resumelens.models import TECHNICAL_CATEGORIES
from resumelens.normalization.transducers import canonicalize, preprocess


class NormalizationStep:
    # Keeps every step of one string, useful to show how it was transformed

    def __init__(self, category, raw, preprocessed, token):
        self.category = category
        self.raw = raw
        self.preprocessed = preprocessed
        self.token = token


class NormalizationResult:

    def __init__(self):
        self.tokens = []
        self.steps = []
        self.unknown = []


def normalize_string(raw, category):
    # "React.js" -> "reactjs" -> "REACT". Returns None when one of the transducers rejects it
    word = preprocess(raw)
    if word is None:
        return None
    return canonicalize(word, category)


def normalize_extraction(extraction):
    # Normalizes all the technical strings of an ExtractionResult
    result = NormalizationResult()
    items = extraction.get_technical_items()
    for category in TECHNICAL_CATEGORIES:
        for raw in items[category]:
            word = preprocess(raw)
            token = None
            if word is not None:
                token = canonicalize(word, category)
            result.steps.append(NormalizationStep(category, raw, word, token))

            if token is None:
                result.unknown.append(raw)
            elif token not in result.tokens:
                # "JS" and "JavaScript" give the same token, it is only kept once
                result.tokens.append(token)
    return result
