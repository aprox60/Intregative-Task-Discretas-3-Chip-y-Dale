import os

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton, EpsilonNFA

from resumelens.classification.automata import EPSILON, ProfileAutomaton
from resumelens.classification.classifier import AUTOMATA, classify
from resumelens.classification.profiles import PROFILES, Profile, QualificationGroup
from resumelens.pipeline import run_resume_pipeline

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_resumes")


def run_sample(filename):
    with open(os.path.join(SAMPLES, filename), encoding="utf-8") as file:
        return run_resume_pipeline(file.read())


def accepted_profiles(result):
    accepted = []
    for name in result.classification:
        if result.classification[name]:
            accepted.append(name)
    return accepted


# Type of each automaton

def test_each_profile_has_the_type_written_in_its_json():
    assert isinstance(AUTOMATA["FULL_STACK_DEVELOPER"].automaton, EpsilonNFA)
    assert isinstance(AUTOMATA["MACHINE_LEARNING_ENGINEER"].automaton, DeterministicFiniteAutomaton)
    assert isinstance(AUTOMATA["BACKEND_DEVELOPER"].automaton, NondeterministicFiniteAutomaton)
    assert isinstance(AUTOMATA["DATA_SCIENTIST"].automaton, EpsilonNFA)


def test_dfa_is_deterministic_and_the_others_are_not():
    assert AUTOMATA["MACHINE_LEARNING_ENGINEER"].automaton.is_deterministic()
    assert not AUTOMATA["BACKEND_DEVELOPER"].automaton.is_deterministic()
    assert not AUTOMATA["FULL_STACK_DEVELOPER"].automaton.is_deterministic()


def test_only_enfa_profiles_have_epsilon_transitions():
    for name in AUTOMATA:
        symbols = []
        for from_state, symbol, to_state in AUTOMATA[name].transitions:
            symbols.append(symbol)
        assert (EPSILON in symbols) == (AUTOMATA[name].automaton_type == "ENFA")


def test_states_and_final_state():
    automaton = AUTOMATA["MACHINE_LEARNING_ENGINEER"]
    assert automaton.states == ["q0", "q1", "q2", "q3", "q4", "q5"]
    assert automaton.start_state == "q0"
    assert automaton.final_states == ["q5"]


def test_nfa_and_dfa_constructions_recognize_the_same_language():
    groups = [QualificationGroup("A", ["X", "Y"]), QualificationGroup("B", ["Z"])]
    nfa = ProfileAutomaton(Profile("TEST", "Test", "", "NFA", "", groups))
    dfa = ProfileAutomaton(Profile("TEST", "Test", "", "DFA", "", groups))
    assert nfa.automaton.is_equivalent_to(dfa.automaton)


# Examples from the assignment

def test_ml_example_from_the_assignment():
    assert classify(["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"], "MACHINE_LEARNING_ENGINEER")


def test_full_stack_example_from_the_assignment():
    assert classify(["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"], "FULL_STACK_DEVELOPER")


# Accepted and rejected sequences

def test_several_tokens_of_the_same_group_are_accepted():
    tokens = ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH", "SQL", "GIT"]
    assert classify(tokens, "MACHINE_LEARNING_ENGINEER")


def test_missing_required_group_is_rejected():
    assert not classify(["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL"], "MACHINE_LEARNING_ENGINEER")


def test_optional_group_can_be_there_or_not():
    without_api = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    with_api = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "REST_API", "GIT"]
    assert classify(without_api, "FULL_STACK_DEVELOPER")
    assert classify(with_api, "FULL_STACK_DEVELOPER")


def test_data_scientist_without_optional_ml_library():
    tokens = ["R", "PANDAS", "STATISTICS", "TABLEAU", "SQL"]
    assert classify(tokens, "DATA_SCIENTIST")


def test_backend_needs_containers():
    tokens = ["JAVA", "SPRING_BOOT", "MYSQL", "REST_API", "GIT"]
    assert not classify(tokens, "BACKEND_DEVELOPER")
    assert classify(["JAVA", "SPRING_BOOT", "MYSQL", "REST_API", "DOCKER", "GIT"], "BACKEND_DEVELOPER")


def test_wrong_order_is_rejected():
    # The automaton expects the canonical order, that is why stage 2 sorts the tokens
    assert not classify(["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"], "FULL_STACK_DEVELOPER")


def test_symbol_outside_the_alphabet_is_rejected():
    assert not classify(["PYTHON", "PANDAS", "DOCKER", "TENSORFLOW", "SQL", "GIT"], "MACHINE_LEARNING_ENGINEER")


def test_empty_sequence_is_rejected():
    for name in PROFILES:
        assert not classify([], name)


def test_missing_groups_explains_the_rejection():
    missing = AUTOMATA["MACHINE_LEARNING_ENGINEER"].missing_groups(["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL"])
    assert missing == ["VERSION_CONTROL"]


# Sample resumes through the whole pipeline

def test_each_sample_is_accepted_only_by_its_profile():
    assert accepted_profiles(run_sample("wednesday_addams.txt")) == ["FULL_STACK_DEVELOPER"]
    assert accepted_profiles(run_sample("mary_jane_watson.txt")) == ["MACHINE_LEARNING_ENGINEER"]
    assert accepted_profiles(run_sample("alex_rivera_backend.txt")) == ["BACKEND_DEVELOPER"]
    assert accepted_profiles(run_sample("nina_patel_data_scientist.txt")) == ["DATA_SCIENTIST"]


def test_a_candidate_can_match_two_profiles():
    assert accepted_profiles(run_sample("kim_possible_multi_profile.txt")) == ["FULL_STACK_DEVELOPER", "BACKEND_DEVELOPER"]


def test_candidates_with_missing_qualifications_are_rejected_by_all():
    assert accepted_profiles(run_sample("invalid_missing_qualification.txt")) == []
    assert accepted_profiles(run_sample("invalid_edge_case.txt")) == []
