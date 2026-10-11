from resumelens.classification.automata import build_automata
from resumelens.classification.profiles import PROFILES, get_profile_names

AUTOMATA = build_automata(PROFILES)

ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"


def classify(tokens, profile_name):
    # Returns True if the profile automaton accepts the sorted token sequence
    automaton = AUTOMATA.get(profile_name.upper())
    if automaton is None:
        raise ValueError("Unknown profile: " + profile_name)
    return automaton.accepts(tokens)


def classify_all_profiles(sorted_by_profile):
    # sorted_by_profile has the sequence of each profile (output of the sorter)
    results = {}
    for profile_name in get_profile_names():
        results[profile_name] = classify(sorted_by_profile[profile_name], profile_name)
    return results


def status_text(accepted):
    if accepted:
        return ACCEPTED
    return REJECTED
