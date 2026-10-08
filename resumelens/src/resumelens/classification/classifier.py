from resumelens.classification.automata import build_default_automata
from resumelens.classification.profiles import PROFILE_CONFIGS, get_profile_names


def classify(tokens, profile_name):
    # Returns True if the profile automaton accepts the token sequence
    automata = build_default_automata(PROFILE_CONFIGS)
    automaton = automata.get(profile_name.upper())
    if automaton is None:
        raise ValueError("Unknown profile: " + profile_name)
    return automaton.accepts(tokens)


def classify_all_profiles(tokens):
    # Checks the tokens against the four profiles
    results = {}
    for profile_name in get_profile_names():
        results[profile_name] = classify(tokens, profile_name)
    return results
