from resumelens.docs_export import transducer_to_markdown, transducer_to_mermaid
from resumelens.normalization.transducers import (
    CATEGORY_TRANSDUCERS,
    END_MARK,
    PREPROCESSING_TRANSDUCER,
    build_category_transducer,
    canonicalize,
    preprocess,
)
from resumelens.normalization.variants import VARIANTS_BY_CATEGORY


# Preprocessing transducer

def test_preprocessing_has_one_state():
    assert PREPROCESSING_TRANSDUCER.states == ["q0"]
    assert PREPROCESSING_TRANSDUCER.start_state == "q0"
    assert PREPROCESSING_TRANSDUCER.final_states == ["q0"]


def test_preprocessing_lowercases_and_deletes_separators():
    assert preprocess("Scikit-learn") == "scikitlearn"
    assert preprocess("Tensor Flow") == "tensorflow"
    assert preprocess("Node.js") == "nodejs"
    assert preprocess("C#") == "c#"
    assert preprocess("power_bi") == "powerbi"


def test_preprocessing_rejects_symbols_outside_sigma():
    assert preprocess("Café") is None
    assert preprocess("C++!") is None


# Category transducers

def test_every_variant_gives_its_canonical_token():
    for category in VARIANTS_BY_CATEGORY:
        variants = VARIANTS_BY_CATEGORY[category]
        for word in variants:
            assert canonicalize(word, category) == variants[word], word


def test_there_is_one_transducer_per_category():
    assert list(CATEGORY_TRANSDUCERS.keys()) == list(VARIANTS_BY_CATEGORY.keys())


def test_a_prefix_of_a_variant_is_rejected():
    # "postgre" is the beginning of "postgres" but it is not a variant
    assert canonicalize("postgre", "databases") is None
    assert canonicalize("reac", "frameworks") is None


def test_a_word_longer_than_a_variant_is_rejected():
    assert canonicalize("reactnative", "frameworks") is None


def test_output_is_only_written_on_the_end_mark():
    transducer = CATEGORY_TRANSDUCERS["databases"]
    for from_state, symbol, to_state, output in transducer.transitions:
        if symbol == END_MARK:
            assert to_state == "qf"
            assert len(output) == 1
        else:
            assert output == []


def test_trie_shares_prefixes():
    # "postgres" and "postgresql" share 8 states, so there are only 2 extra states for "ql"
    small = build_category_transducer("test", {"postgres": "POSTGRESQL"})
    both = build_category_transducer("test", {"postgres": "POSTGRESQL", "postgresql": "POSTGRESQL"})
    assert len(both.states) == len(small.states) + 2


def test_category_transducers_are_deterministic():
    for category in CATEGORY_TRANSDUCERS:
        seen = []
        for from_state, symbol, to_state, output in CATEGORY_TRANSDUCERS[category].transitions:
            assert (from_state, symbol) not in seen
            seen.append((from_state, symbol))


# Formal definition and diagram

def test_markdown_has_the_seven_parts():
    text = transducer_to_markdown(CATEGORY_TRANSDUCERS["tools"])
    for part in ["**Q**", "**Σ**", "**Γ**", "**δ**", "**ω**", "**q0**", "**F**"]:
        assert part in text
    assert "POWER_BI" in text


def test_mermaid_diagram_marks_the_final_state():
    text = transducer_to_mermaid(CATEGORY_TRANSDUCERS["tools"])
    assert text.startswith("```mermaid")
    assert "qf(((qf)))" in text
