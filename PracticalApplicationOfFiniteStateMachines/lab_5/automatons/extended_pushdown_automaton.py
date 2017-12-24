from automatons.automaton import Automaton


class ExtendedPushdownAutomaton(Automaton):
    START_STATE = 'q'
    FINAL_STATE = 'r'
    START_STACK_SYMBOL = '_'

    def __init__(
        self,
        stack_symbols,
        input_symbols,
        transitions,
        grammar,
        input_sequence=None,
        stack=None,
        level=0,
        logger=None
    ):
        super().__init__(logger)
        self.stack_symbols = stack_symbols
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.grammar = grammar
        self.input_sequence = input_sequence if input_sequence is not None else ''
        self.stack = stack or [self.START_STACK_SYMBOL]
        self.states = {self.START_STATE, self.FINAL_STATE}
        self.current_state = self.START_STATE
        self.level = level

    @staticmethod
    def from_grammar(grammar):
        """Context-free grammar to extended pushdown automaton"""
        start_state = ExtendedPushdownAutomaton.START_STATE
        final_state = ExtendedPushdownAutomaton.FINAL_STATE
        start_stack_symbol = ExtendedPushdownAutomaton.START_STACK_SYMBOL

        stack_symbols = (
            grammar.terminals |
            grammar.nonterminals |
            {start_stack_symbol}
        )
        input_symbols = grammar.terminals
        transitions = set()
        for rule in grammar.rules:
            transition = (start_state, None, tuple(list(rule.output_symbols))), (start_state, rule.input_symbols)
            transitions.add(transition)
        for terminal in grammar.terminals:
            transition = (start_state, terminal, None), (start_state, terminal)
            transitions.add(transition)
        transitions.add((
            (start_state, None, (start_stack_symbol, grammar.start_symbol)),
            (final_state, None)
        ))
        return ExtendedPushdownAutomaton(
            grammar=grammar,
            stack_symbols=stack_symbols,
            input_symbols=input_symbols,
            transitions=transitions
        )

    @property
    def is_in_accepted_state(self):
        return self.current_state == self.FINAL_STATE

    def input_sequence_head(self, depth=1):
        return self.input_sequence[:depth]

    def stack_head(self, depth=1):
        return tuple(self.stack[-depth:])

    def set_input_sequence(self, input_sequence):
        """Set input sequence for automaton"""
        self.input_sequence = input_sequence
        self.current_state = self.START_STATE
        self.stack = [self.START_STACK_SYMBOL]

    def start(self):
        """Try to find sequence of transitions to final state"""
        transitions = self._filter_transitions()

        self._log([
            ("START level", self.level),
            ("Accepted transitions", '\n'.join(map(repr, self._order_transitions(transitions)))),
            ("Input sequence", repr(self.input_sequence)),
            ("Stack", repr(self.stack))
        ])

        if not transitions:
            return False

        for transition in transitions:
            _, (new_state, _) = transition
            if new_state == self.FINAL_STATE:
                self._apply(transition)
                return True

        alternative_automata = map(self._copy_and_apply, transitions)
        return any(a.start() for a in alternative_automata)

    def _copy(self):
        return ExtendedPushdownAutomaton(
            stack_symbols=self.stack_symbols.copy(),
            input_symbols=self.input_symbols.copy(),
            transitions=self.transitions.copy(),
            grammar=self.grammar,
            input_sequence=self.input_sequence,
            stack=self.stack[:],
            level=self.level + 1,
            logger=self.logger
        )

    def _pop_stack(self, depth=1):
        stack_head = self.stack_head(depth)
        self.stack = self.stack[:-depth]
        return tuple(stack_head)

    def _pick_input(self, depth=1):
        input_sequence_head = self.input_sequence_head(depth)
        self.input_sequence = self.input_sequence[depth:]
        return input_sequence_head

    def _apply(self, transition):
        (state, input_sequence_head, stack_head), (new_state, new_stack_head) = transition

        assert state == self.current_state
        assert input_sequence_head is None or input_sequence_head == self.input_sequence_head(depth=len(input_sequence_head))
        assert stack_head is None or stack_head == self.stack_head(depth=len(stack_head))

        # Clear old state
        if input_sequence_head is not None:
            self._pick_input(depth=len(input_sequence_head))
        if stack_head is not None:
            self._pop_stack(depth=len(stack_head))

        # Set new state
        if new_stack_head is not None:
            self.stack += new_stack_head
        self.current_state = new_state

        return self

    def _copy_and_apply(self, transition):
        return self._copy()._apply(transition)

    def _filter_transitions(self):
        transitions = []
        for transition in self.transitions:
            (state, input_sequence_head, stack_head), (new_state, new_tos) = transition

            if state != self.current_state:
                continue

            if input_sequence_head is not None and input_sequence_head != self.input_sequence_head(depth=len(input_sequence_head)):
                continue

            if stack_head is not None and stack_head != self.stack_head(depth=len(stack_head)):
                continue

            transitions.append(transition)
        return transitions

    def _order_transitions(self, transitions):
        return sorted(list(transitions), key=lambda t: len(t[0][2] or []), reverse=True)
