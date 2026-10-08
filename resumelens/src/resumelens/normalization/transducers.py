# Stage 2: finite-state transducers built with pyformlang.
#
# Each transducer is M = (Q, Sigma, Gamma, delta, omega, q0, F). We build the pyformlang FST
# and we also keep every part of the 7-tuple, so we can print the formal definition and
# draw the diagram from the same object.
#
# Two kinds of transducers are used:
# 1. PREPROCESSING: one state. It changes upper case letters to lower case and deletes the
#    separators (space, ".", "-", "_", "/"). "Scikit-learn" -> "scikitlearn"
# 2. One transducer per technical category. It reads the preprocessed word character by
#    character (a trie) and when it reads the end mark "$" it writes the canonical token.
#    "scikitlearn$" -> SCIKIT_LEARN

import string

from pyformlang.fst import FST

from resumelens.normalization.variants import VARIANTS_BY_CATEGORY

# End of word mark. Without it the transducer could not know if "postgres" ends there
# or if it continues as "postgresql"
END_MARK = "$"

SEPARATORS = [" ", ".", "-", "_", "/"]
KEPT_SYMBOLS = ["+", "#"]


class Transducer:

    def __init__(self, name):
        self.name = name
        self.fst = FST()
        self.states = []
        self.input_alphabet = []
        self.output_alphabet = []
        # Each transition is (from_state, input_symbol, to_state, output_list)
        self.transitions = []
        self.start_state = None
        self.final_states = []

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)

    def set_start_state(self, state):
        self.add_state(state)
        self.start_state = state
        self.fst.add_start_state(state)

    def add_final_state(self, state):
        self.add_state(state)
        if state not in self.final_states:
            self.final_states.append(state)
        self.fst.add_final_state(state)

    def add_transition(self, from_state, symbol, to_state, output):
        self.add_state(from_state)
        self.add_state(to_state)
        if symbol not in self.input_alphabet:
            self.input_alphabet.append(symbol)
        for out_symbol in output:
            if out_symbol not in self.output_alphabet:
                self.output_alphabet.append(out_symbol)
        self.transitions.append((from_state, symbol, to_state, output))
        self.fst.add_transition(from_state, symbol, to_state, output)

    def translate(self, symbols):
        # Returns the output of the first accepted path, or None if the input is rejected
        for output in self.fst.translate(symbols):
            return output
        return None


def build_preprocessing_transducer():
    transducer = Transducer("PREPROCESSING")
    transducer.set_start_state("q0")
    transducer.add_final_state("q0")

    for letter in string.ascii_uppercase:
        transducer.add_transition("q0", letter, "q0", [letter.lower()])
    for letter in string.ascii_lowercase:
        transducer.add_transition("q0", letter, "q0", [letter])
    for digit in string.digits:
        transducer.add_transition("q0", digit, "q0", [digit])
    for symbol in KEPT_SYMBOLS:
        transducer.add_transition("q0", symbol, "q0", [symbol])
    # The separators are deleted: their output is the empty string (epsilon)
    for separator in SEPARATORS:
        transducer.add_transition("q0", separator, "q0", [])
    return transducer


def build_category_transducer(category, variants):
    # Builds a trie: words with the same prefix share the first states
    transducer = Transducer(category)
    transducer.set_start_state("q0")
    transducer.add_final_state("qf")

    next_state_number = 1
    children = {}
    for word in variants:
        state = "q0"
        for character in word:
            key = (state, character)
            if key not in children:
                children[key] = "q" + str(next_state_number)
                next_state_number = next_state_number + 1
                # While reading the word the transducer writes nothing (epsilon)
                transducer.add_transition(state, character, children[key], [])
            state = children[key]
        # At the end of the word it writes the canonical token
        transducer.add_transition(state, END_MARK, "qf", [variants[word]])
    return transducer


def build_all_category_transducers():
    transducers = {}
    for category in VARIANTS_BY_CATEGORY:
        transducers[category] = build_category_transducer(category, VARIANTS_BY_CATEGORY[category])
    return transducers


PREPROCESSING_TRANSDUCER = build_preprocessing_transducer()
CATEGORY_TRANSDUCERS = build_all_category_transducers()


def preprocess(text):
    # "React.js" -> "reactjs". Returns None if the text has a character outside Sigma
    output = PREPROCESSING_TRANSDUCER.translate(list(text))
    if output is None:
        return None
    return "".join(output)


def canonicalize(word, category):
    # "reactjs" -> "REACT". Returns None if the word is not a known variant of the category
    transducer = CATEGORY_TRANSDUCERS[category]
    output = transducer.translate(list(word) + [END_MARK])
    if output is None or len(output) == 0:
        return None
    return output[0]
