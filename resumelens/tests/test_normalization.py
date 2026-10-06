from resumelens.normalization.lexicon import normalize_tokens
from resumelens.normalization.sorter import sort_tokens


def test_variant_normalization():
    tokens = ["Javascript", "JS", "Node.js", "Postgres", "scikit-learn", "PyTorch"]
    normalized = normalize_tokens(tokens)
    assert "JAVASCRIPT" in normalized
    assert "NODE_JS" in normalized
    assert "POSTGRESQL" in normalized
    assert "SCIKIT_LEARN" in normalized
    assert "PYTORCH" in normalized


def test_profile_ordering_is_stable():
    tokens = ["GIT", "NODE_JS", "JS", "POSTGRESQL", "REACT"]
    ordered = sort_tokens(tokens, "FULL_STACK_DEVELOPER")
    assert ordered.index("JAVASCRIPT") < ordered.index("REACT")
    assert ordered.index("REACT") < ordered.index("NODE_JS")
    assert ordered.index("NODE_JS") < ordered.index("POSTGRESQL")
    assert ordered.index("POSTGRESQL") < ordered.index("GIT")
