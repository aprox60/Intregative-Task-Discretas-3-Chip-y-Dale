from resumelens.classification.classifier import classify


def test_ml_reference_automaton_accepts_reference_pattern():
    tokens = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
    assert classify(tokens, "MACHINE_LEARNING_ENGINEER") is True


def test_full_stack_reference_automaton_accepts_reference_pattern():
    tokens = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    assert classify(tokens, "FULL_STACK_DEVELOPER") is True


def test_missing_required_qualification_is_rejected():
    tokens = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL"]
    assert classify(tokens, "MACHINE_LEARNING_ENGINEER") is False
