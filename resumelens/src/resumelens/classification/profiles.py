from __future__ import annotations

PROFILE_CONFIGS: dict[str, dict[str, object]] = {
    "FULL_STACK_DEVELOPER": {
        "name": "FULL_STACK_DEVELOPER",
        "required_tokens": ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        "sequence": [
            ["JAVASCRIPT", "TYPESCRIPT"],
            ["REACT", "ANGULAR", "VUE"],
            ["NODE_JS", "DJANGO", "SPRING_BOOT"],
            ["SQL", "POSTGRESQL", "MONGODB"],
            ["GIT"],
        ],
        "description": "Checks whether a candidate has explicit frontend, backend, storage, and version-control evidence.",
    },
    "MACHINE_LEARNING_ENGINEER": {
        "name": "MACHINE_LEARNING_ENGINEER",
        "required_tokens": ["PYTHON", "PANDAS", "SCIKIT_LEARN", "POSTGRESQL", "GIT"],
        "sequence": [
            ["PYTHON"],
            ["PANDAS", "NUMPY"],
            ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"],
            ["SQL", "POSTGRESQL"],
            ["GIT"],
        ],
        "description": "Checks whether a candidate has explicit ML workflow evidence: Python, data libraries, ML frameworks, SQL, and Git.",
    },
    "PROFILE_3_TODO": {
        "name": "PROFILE_3_TODO",
        "required_tokens": ["TODO"],
        "sequence": [["TODO"]],
        "description": "Placeholder for a software-engineering or DevOps profile. Fill in after the final profile definition is selected.",
    },
    "PROFILE_4_TODO": {
        "name": "PROFILE_4_TODO",
        "required_tokens": ["TODO"],
        "sequence": [["TODO"]],
        "description": "Placeholder for an AI/data profile such as Data Engineer or NLP Engineer. Fill in after the final profile definition is selected.",
    },
}


def get_profile_names() -> list[str]:
    """Return profile names in the project order: Full Stack, ML, Profile 3, Profile 4."""

    return [
        "FULL_STACK_DEVELOPER",
        "MACHINE_LEARNING_ENGINEER",
        "PROFILE_3_TODO",
        "PROFILE_4_TODO",
    ]
