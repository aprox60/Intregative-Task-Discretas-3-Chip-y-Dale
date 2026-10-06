"""Classification stage package."""

from resumelens.classification.automata import ProfileAutomaton, build_default_automata, build_profile_automaton
from resumelens.classification.classifier import classify, classify_all_profiles
from resumelens.classification.profiles import PROFILE_CONFIGS, get_profile_names

__all__ = [
    "ProfileAutomaton",
    "build_default_automata",
    "build_profile_automaton",
    "classify",
    "classify_all_profiles",
    "PROFILE_CONFIGS",
    "get_profile_names",
]
