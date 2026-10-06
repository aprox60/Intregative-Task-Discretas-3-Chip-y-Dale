from __future__ import annotations

from resumelens.classification.automata import build_default_automata
from resumelens.classification.profiles import PROFILE_CONFIGS


def classify(tokens: list[str], profile_name: str) -> bool:
    """Return True if the normalized token stream matches the given profile automaton."""

    automata = build_default_automata(PROFILE_CONFIGS)
    automaton = automata.get(profile_name.upper())
    if automaton is None:
        raise ValueError(f"Unknown profile: {profile_name}")
    return automaton.accepts(tokens)


def classify_all_profiles(tokens: list[str]) -> dict[str, bool]:
    """Classify a token list against all four project profiles."""

    return {
        profile_name: classify(tokens, profile_name)
        for profile_name in [
            "FULL_STACK_DEVELOPER",
            "MACHINE_LEARNING_ENGINEER",
            "PROFILE_3_TODO",
            "PROFILE_4_TODO",
        ]
    }


def classify_reference_ml(tokens: list[str]) -> bool:
    """Reference example for the ML engineer profile.

    Input example: ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"] -> ACCEPTED.
    """

    return classify(tokens, "MACHINE_LEARNING_ENGINEER")
