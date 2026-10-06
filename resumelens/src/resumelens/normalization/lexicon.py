from __future__ import annotations

import re


DEFAULT_LEXICON: dict[str, str] = {
    "js": "JAVASCRIPT",
    "javascript": "JAVASCRIPT",
    "java script": "JAVASCRIPT",
    "react.js": "REACT",
    "reactjs": "REACT",
    "react js": "REACT",
    "node.js": "NODE_JS",
    "nodejs": "NODE_JS",
    "node js": "NODE_JS",
    "postgres": "POSTGRESQL",
    "postgresql": "POSTGRESQL",
    "pandas": "PANDAS",
    "sklearn": "SCIKIT_LEARN",
    "scikit learn": "SCIKIT_LEARN",
    "scikit-learn": "SCIKIT_LEARN",
    "tensor flow": "TENSORFLOW",
    "tensorflow": "TENSORFLOW",
    "py torch": "PYTORCH",
    "pytorch": "PYTORCH",
    "git": "GIT",
    "sql": "SQL",
    "numpy": "NUMPY",
    "python": "PYTHON",
}


def normalize_key(value: str) -> str:
    """Normalize a skill label to the lexical form used by the dictionary."""

    cleaned = value.strip().lower()
    cleaned = cleaned.replace("_", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.replace("-", " ")
    return cleaned


def build_lexicon() -> dict[str, str]:
    """Return the canonical skill lexicon used by the FST and sorters."""

    return DEFAULT_LEXICON.copy()


def normalize_token(token: str, lexicon: dict[str, str] | None = None) -> str:
    """Map a token to its canonical symbol or preserve a stable upper-case fallback."""

    mapping = lexicon or build_lexicon()
    key = normalize_key(token)
    if key in mapping:
        return mapping[key]
    fallback = re.sub(r"[^A-Za-z0-9]+", "_", token.strip()).upper().strip("_")
    return fallback or token.strip().upper()


def normalize_tokens(tokens: list[str], lexicon: dict[str, str] | None = None) -> list[str]:
    """Normalize a list of tokens and return a canonical list."""

    result: list[str] = []
    mapping = lexicon or build_lexicon()
    for token in tokens:
        canonical = normalize_token(token, mapping)
        if canonical and canonical not in result:
            result.append(canonical)
    return result
