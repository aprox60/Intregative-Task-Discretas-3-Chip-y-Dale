# Stage 3: finite automata that recognize the qualification pattern of each profile.
#
# Each automaton is M = (Q, Sigma, delta, q0, F) built with pyformlang from the profile
# groups. The input is the sorted sequence of tokens from stage 2, so the automaton only
# has to check that the groups appear in order and that no required group is missing.
#
# With n groups G0, G1, ..., G(n-1) the states are q0, q1, ..., qn and F = {qn}.
# Being in state qi means "groups G0 ... G(i-1) are already satisfied".
#
# The three types of automata are built in a different way:
# - DFA:  delta(qi, t) = q(i+1) and delta(q(i+1), t) = q(i+1) for t in Gi
#         (the loop reads more tokens of the same group)
# - NFA:  delta(qi, t) = {qi, q(i+1)} for t in Gi
#         (after reading t it can stay or move on, so it has to "guess")
# - ENFA: like the DFA, plus delta(qi, epsilon) = {q(i+1)} when Gi is optional
#         (the epsilon transition skips the group)

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    Epsilon,
    EpsilonNFA,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)

EPSILON = "ε"


class ProfileAutomaton:

    def __init__(self, profile):
        self.profile = profile
        self.automaton_type = profile.automaton_type
        self.states = []
        self.alphabet = profile.get_alphabet()
        # Each transition is (from_state, symbol, to_state). The symbol is EPSILON for epsilon moves
        self.transitions = []
        self.start_state = "q0"
        self.final_states = []

        if self.automaton_type == "DFA":
            self.automaton = DeterministicFiniteAutomaton()
        elif self.automaton_type == "NFA":
            self.automaton = NondeterministicFiniteAutomaton()
        else:
            self.automaton = EpsilonNFA()

        self.build()

    def add_transition(self, from_state, symbol, to_state):
        self.transitions.append((from_state, symbol, to_state))
        if symbol == EPSILON:
            self.automaton.add_transition(State(from_state), Epsilon(), State(to_state))
        else:
            self.automaton.add_transition(State(from_state), Symbol(symbol), State(to_state))

    def build(self):
        groups = self.profile.groups
        for number in range(len(groups) + 1):
            self.states.append("q" + str(number))

        for number in range(len(groups)):
            group = groups[number]
            current = "q" + str(number)
            following = "q" + str(number + 1)

            for token in group.tokens:
                if self.automaton_type == "NFA":
                    self.add_transition(current, token, current)
                    self.add_transition(current, token, following)
                else:
                    self.add_transition(current, token, following)
                    self.add_transition(following, token, following)

            if not group.required:
                self.add_transition(current, EPSILON, following)

        last_state = self.states[len(self.states) - 1]
        self.final_states.append(last_state)
        self.automaton.add_start_state(State(self.start_state))
        self.automaton.add_final_state(State(last_state))

    def accepts(self, tokens):
        symbols = []
        for token in tokens:
            symbols.append(Symbol(token))
        return self.automaton.accepts(symbols)

    def missing_groups(self, tokens):
        # Explains a rejection: the required groups that have no token in the sequence
        missing = []
        for group in self.profile.groups:
            if not group.required:
                continue
            found = False
            for token in group.tokens:
                if token in tokens:
                    found = True
            if not found:
                missing.append(group.name)
        return missing


def build_automata(profiles):
    automata = {}
    for name in profiles:
        automata[name] = ProfileAutomaton(profiles[name])
    return automata
