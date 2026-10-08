import json
import os

# Folder that contains the profile JSON files
PROFILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profiles")

# Project order: the two profiles from the assignment first, then ours
PROFILE_FILES = [
    "full_stack.json",
    "ml_engineer.json",
    "backend_developer.json",
    "data_scientist.json",
]

AUTOMATON_TYPES = ["DFA", "NFA", "ENFA"]


class QualificationGroup:
    # One block of the profile pattern, for example FRONTEND_FRAMEWORK = {REACT, ANGULAR, VUE}

    def __init__(self, name, tokens, required=True):
        self.name = name
        self.tokens = tokens
        self.required = required


class Profile:
    # A professional profile is an ordered list of qualification groups

    def __init__(self, name, display_name, area, automaton_type, description, groups):
        self.name = name
        self.display_name = display_name
        self.area = area
        self.automaton_type = automaton_type
        self.description = description
        self.groups = groups

    def get_alphabet(self):
        # All the tokens of the profile, in group order
        alphabet = []
        for group in self.groups:
            for token in group.tokens:
                alphabet.append(token)
        return alphabet


def load_profile(path):
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    name = data["name"]
    groups = []
    used_tokens = []
    for group_data in data["groups"]:
        required = group_data.get("required", True)
        group = QualificationGroup(group_data["name"], group_data["tokens"], required)

        # A token can't be in two groups, otherwise the canonical order would be ambiguous
        for token in group.tokens:
            if token in used_tokens:
                raise ValueError("Profile " + name + ": token " + token + " is in more than one group")
            used_tokens.append(token)
        groups.append(group)

    automaton_type = data.get("automaton_type", "DFA").upper()
    if automaton_type not in AUTOMATON_TYPES:
        raise ValueError("Profile " + name + ": unknown automaton type " + automaton_type)

    # Optional groups are skipped with epsilon transitions, so they only work in an ENFA
    for group in groups:
        if not group.required and automaton_type != "ENFA":
            raise ValueError("Profile " + name + ": optional groups need an ENFA")

    return Profile(
        name,
        data.get("display_name", name),
        data.get("area", ""),
        automaton_type,
        data.get("description", ""),
        groups,
    )


def load_profiles():
    profiles = {}
    for filename in PROFILE_FILES:
        profile = load_profile(os.path.join(PROFILES_DIR, filename))
        profiles[profile.name] = profile
    return profiles


PROFILES = load_profiles()


def get_profile_names():
    return list(PROFILES.keys())


# Temporary version for the current automaton builder:
# only the required groups, as a sequence
PROFILE_CONFIGS = {}
for profile_name in PROFILES:
    sequence = []
    for group in PROFILES[profile_name].groups:
        if group.required:
            sequence.append(group.tokens)
    PROFILE_CONFIGS[profile_name] = {
        "name": profile_name,
        "sequence": sequence,
        "description": PROFILES[profile_name].description,
    }
