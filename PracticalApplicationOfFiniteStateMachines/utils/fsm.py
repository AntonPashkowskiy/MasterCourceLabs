#!/usr/bin/python3


class FiniteStateMachine:
    def __init__(self, states, input_sumbols, transitions, start_state, final_state):
        self.states = states
        self.input_symbols = input_sumbols
        self.transitions = transitions
        self.start_state = start_state
        self.final_state = final_state

    @staticmethod
    def get_from_grammar(grammar):
        pass

    @staticmethod
    def get_determined_from_grammar(grammar):
        pass

    def to_determined(self):
        pass

    def is_determined(self):
        pass

    def to_graph_image(self):
        pass
