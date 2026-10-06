from __future__ import annotations

from resumelens.normalization.lexicon import normalize_token

PROFILE_SORT_ORDERS = {
    "FULL_STACK_DEVELOPER": [
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
        "SQL",
        "DJANGO",
        "SPRING_BOOT",
    ],
    "MACHINE_LEARNING_ENGINEER": [
        "PYTHON",
        "PANDAS",
        "NUMPY",
        "SCIKIT_LEARN",
        "TENSORFLOW",
        "PYTORCH",
        "SQL",
        "POSTGRESQL",
        "GIT",
    ],
}


def sort_tokens(tokens: list[str], profile_name: str) -> list[str]:
    """Sort canonical tokens according to a profile-specific order.

    The profile order is intentionally explicit and deterministic. This ensures that the
    automata operate on a consistent sequence before classification.
    """

    canonical_tokens = [normalize_token(token) for token in tokens]
    order = PROFILE_SORT_ORDERS.get(profile_name.upper(), [])
    if not order:
        return sorted(set(canonical_tokens))

    ranked = {token: index for index, token in enumerate(order)}
    result = sorted(set(canonical_tokens), key=lambda token: (ranked.get(token, len(order)), token))
    return result


def sort_candidates(tokens: list[str], profile_name: str | None = None) -> list[str]:
    """Sort tokens for a chosen profile or for the default ordering if no profile is provided."""

    if profile_name is None:
        return sorted(set(tokens))
    return sort_tokens(tokens, profile_name)
