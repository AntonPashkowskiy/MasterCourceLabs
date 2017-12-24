from automatons.automaton import Automaton


class PushdownAutomaton(Automaton):
    default_state = 'q'

    def __init__(
        self,
        stack_symbols,
        input_symbols,
        transitions,
        stack=None,
        input_sequence=None,
        level=0,
        grammar=None,
        logger=None
    ):
        super().__init__(logger)
        self.states = {self.default_state}
        self.start_state = self.default_state
        self.stack_symbols = stack_symbols
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.stack = stack or []
        self.input_sequence = input_sequence or None
        self.level = level
        self.grammar = grammar

    @staticmethod
    def from_grammar(grammar):
        """Context-free grammar to extended pushdown automaton"""
        state = PushdownAutomaton.default_state
        stack_symbols = grammar.terminals | grammar.nonterminals
        input_symbols = grammar.terminals
        transitions = set()
        for rule in grammar.rules:
            transition = (state, None, rule.input_symbols), (state, tuple(list(rule.output_symbols)[::-1]))
            transitions.add(transition)
        for input_symbol in input_symbols:
            transition = (state, input_symbol, input_symbol), (state, None)
            transitions.add(transition)
        return PushdownAutomaton(
            stack_symbols=stack_symbols,
            input_symbols=input_symbols,
            transitions=transitions,
            stack=[grammar.start_symbol],
            grammar=grammar
        )

    @property
    def stack_head(self):
        if self.stack:
            return self.stack[-1]

    @property
    def input_sequence_head(self):
        return self.input_sequence[0]

    def __str__(self):
        current_class = self.__class__.__name__
        input_content = repr(self.input_sequence)
        stack_content = self.stack[::-1]
        return f"{current_class}:\n    Input: {input_content}\n    Stack: {stack_content}\n"

    def set_input_sequence(self, input_sequence):
        """Set input sequence for automaton"""
        assert set(input_sequence).issubset(self.input_symbols)
        self.stack = [self.grammar.start_symbol]
        self.input_sequence = input_sequence

    def start(self):
        """Try to find sequence of transitions to empty automaton"""
        assert self.input_sequence is not None
        if not self.input_sequence and not self.stack:
            return True

        if not self.input_sequence:
            return False

        if len(self.input_sequence) < len(self.stack):
            return False

        transitions = self._filter_transitions()
        if not transitions:
            return False

        alternative_automata = map(self._copy_and_apply, transitions)
        return any(a.start() for a in alternative_automata)

    def _copy(self):
        return PushdownAutomaton(
            stack_symbols=self.stack_symbols.copy(),
            input_symbols=self.input_symbols.copy(),
            transitions=self.transitions.copy(),
            stack=self.stack[:],
            input_sequence=self.input_sequence,
            level=self.level + 1,
            grammar=self.grammar,
            logger=self.logger
        )

    def _pick_input_head(self):
        input_sequence_head = self.input_sequence_head
        self.input_sequence = self.input_sequence[1:]
        return input_sequence_head

    def _apply(self, transition):
        apply_start_state = [
            ("APPLY level", self.level),
            ("Input sequence", repr(self.input_sequence)),
            ("Stack", repr(self.stack)),
            ("Transition", transition)
        ]

        (_, input_symbol, stack_head), (_, new_stack_head) = transition
        assert (input_symbol is None or input_symbol == self.input_sequence_head) and stack_head == self.stack_head

        # Clear old state
        if input_symbol is not None:
            self._pick_input_head()
        self.stack.pop()

        # Set new state
        if new_stack_head is not None:
            self.stack += new_stack_head

        apply_final_state = [
            ("APPLY RESULT level", self.level),
            ("Input sequence", repr(self.input_sequence)),
            ("Stack", repr(self.stack))
        ]
        self._log(apply_start_state.extend(apply_final_state))
        return self

    def _copy_and_apply(self, transition):
        return self._copy()._apply(transition)

    def _filter_transitions(self):
        transitions = []
        for transition in self.transitions:
            (_, input_symbol, stack_head), (_, new_stack_head) = transition
            # Transitions which allows move to the next automatron state
            if input_symbol in (self.input_sequence_head, None) and stack_head == self.stack_head:
                transitions.append(transition)

        self._log([
            ("FILTER level", self.level),
            ("Input sequence", repr(self.input_sequence)),
            ("Stack", repr(self.stack)),
            ("Transitions", transitions)
        ])
        return transitions
