from __future__ import annotations

from dataclasses import dataclass

try:
    from pyformlang.finite_automaton import NFA
except Exception:  # pragma: no cover
    NFA = None


@dataclass
class ProfileAutomaton:
    """A lightweight automaton wrapper used to classify normalized tokens."""

    profile_name: str
    states: list[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], set[str]]
    start_state: str
    accepting_states: set[str]

    def accepts(self, tokens: list[str]) -> bool:
        """Check whether the token stream is accepted by the automaton."""

        if not tokens:
            return False
        current = {self.start_state}
        for token in tokens:
            next_states: set[str] = set()
            for state in current:
                for symbol in self.transitions.get((state, token), set()):
                    next_states.add(symbol)
            current = next_states
            if not current:
                return False
        return bool(current & self.accepting_states)


def build_profile_automaton(profile_config: dict[str, object]) -> ProfileAutomaton:
    """Construct a profile automaton from a config dictionary.

    The project intentionally can operate with a small custom automaton wrapper and still
    document the pyformlang-based formal model in the design docs. This is a practical
    skeleton for the assignment.
    """

    name = str(profile_config.get("name", "UNKNOWN"))
    states = [f"q{i}" for i in range(0, len(profile_config.get("sequence", [])) + 2)]
    alphabet = set()
    transitions: dict[tuple[str, str], set[str]] = {}
    sequence = profile_config.get("sequence", [])
    states = [f"q{i}" for i in range(0, len(sequence) + 1)]

    for idx, segment in enumerate(sequence):
        for token in segment:
            alphabet.add(str(token))
            current = states[idx]
            target = states[idx + 1]
            transitions.setdefault((current, str(token)), set()).add(target)

    start_state = states[0]
    accepting_states = {states[-1]}

    return ProfileAutomaton(
        profile_name=name,
        states=states,
        alphabet=alphabet,
        transitions=transitions,
        start_state=start_state,
        accepting_states=accepting_states,
    )


def build_default_automata(profile_configs: dict[str, dict[str, object]]) -> dict[str, ProfileAutomaton]:
    """Return all project automata keyed by profile name."""

    return {name: build_profile_automaton(config) for name, config in profile_configs.items()}
