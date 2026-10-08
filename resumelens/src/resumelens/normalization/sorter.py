# Stage 2: puts the normalized tokens in the canonical order of a profile.
#
# The order is the order of the profile groups (for Full Stack: frontend language,
# frontend framework, backend, database, API, version control). Inside a group, the
# order in which the tokens are written in the JSON file.
# Tokens that are not part of the profile are left out, so the automaton only reads
# symbols of its own alphabet. This way the result does not depend on the order in
# which the candidate wrote the skills.
#
# Example (Full Stack): GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT
#                    -> JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT


def sort_for_profile(tokens, profile):
    sorted_tokens = []
    for token in profile.get_alphabet():
        if token in tokens:
            sorted_tokens.append(token)
    return sorted_tokens


def sort_for_all_profiles(tokens, profiles):
    result = {}
    for name in profiles:
        result[name] = sort_for_profile(tokens, profiles[name])
    return result
