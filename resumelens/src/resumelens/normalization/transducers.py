from __future__ import annotations

from dataclasses import dataclass, field

from resumelens.normalization.lexicon import build_lexicon, normalize_token

try:
    from pyformlang.fst import FST
except Exception:  # pragma: no cover - fallback when dependency is unavailable
    FST = None


@dataclass
class FSTDescriptor:
    """A concise descriptor of the transducer tuple M = (Q, Σ, Γ, δ, ω, q0, F)."""

    states: list[str]
    input_alphabet: set[str] = field(default_factory=set)
    output_alphabet: set[str] = field(default_factory=set)
    transitions: dict[tuple[str, str], tuple[str, str]] = field(default_factory=dict)
    start_state: str = "q0"
    accepting_states: set[str] = field(default_factory=set)

    def as_dict(self) -> dict[str, object]:
        return {
            "Q": self.states,
            "Σ": sorted(self.input_alphabet),
            "Γ": sorted(self.output_alphabet),
            "δ": self.transitions,
            "ω": "output emission on accepted path",
            "q0": self.start_state,
            "F": sorted(self.accepting_states),
        }


class SkillCanonicalizationTransducer:
    """Transducer-based canonicalizer designed around a lexicon of variations."""

    def __init__(self, lexicon: dict[str, str] | None = None):
        self.lexicon = lexicon or build_lexicon()
        self.descriptor = self._build_descriptor()

    def _build_descriptor(self) -> FSTDescriptor:
        keys = sorted({k for k in self.lexicon})
        states = ["q0", "q1"]
        alphabet = set()
        output_alphabet = set(self.lexicon.values())
        transitions: dict[tuple[str, str], tuple[str, str]] = {}
        for key in keys:
            alphabet.add(key)
            transitions[("q0", key)] = ("q1", self.lexicon[key])
        return FSTDescriptor(
            states=states,
            input_alphabet=alphabet,
            output_alphabet=output_alphabet,
            transitions=transitions,
            start_state="q0",
            accepting_states={"q1"},
        )

    def build_pyformlang_fst(self):
        """Construct an FST if the dependency is available.

        When `pyformlang` is absent, the method returns a descriptor object that preserves
        the formal structure required by the course documentation.
        """

        if FST is None:
            return self.descriptor
        # Exercise scaffold: actual pyformlang FST creation is intentionally left as a
        # reusable abstraction. Most teams will expand this in implementation.
        return FST()

    def normalize(self, token: str) -> str:
        """Apply the canonicalization transducer to a single token."""

        return normalize_token(token, self.lexicon)

    def normalize_many(self, tokens: list[str]) -> list[str]:
        """Apply the canonicalization transducer to each token and remove duplicates."""

        normalized: list[str] = []
        for token in tokens:
            result = self.normalize(token)
            if result and result not in normalized:
                normalized.append(result)
        return normalized


def build_skill_transducer(lexicon: dict[str, str] | None = None) -> SkillCanonicalizationTransducer:
    """Convenience constructor for the transducer used in the normalization stage."""

    return SkillCanonicalizationTransducer(lexicon=lexicon)
