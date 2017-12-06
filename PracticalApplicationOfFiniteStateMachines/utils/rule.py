#!/usr/bin/python3
EMPTY_SEQUNCE = 'ε'


class Rule:
    def __init__(self, input_symbols, output_symbols):
        if input_symbols is None or output_symbols is None:
            raise ValueError("Invalid rule arguments")
        self._input_symbols = input_symbols
        self._output_symbols = output_symbols

    @property
    def input_symbols(self):
        return self._input_symbols

    @property
    def output_symbols(self):
        return self._output_symbols

    def is_regular(self, context):
        """Check if rule grammar is regular."""
        terminals, nonterminals = context
        return (
            self.is_context_free(context) and
            (
                len(self._output_symbols) == 2 and
                set(self._output_symbols) & terminals and
                set(self._output_symbols) & nonterminals
            ) or (
                len(self._output_symbols) == 1 and
                set(self._output_symbols) <= nonterminals | terminals | {EMPTY_SEQUNCE}
            )
        )

    def is_context_free(self, context):
        """Check if the grammar rule is context-free."""
        _, nonterminals = context
        return len(self._input_symbols) == 1 and self._input_symbols in nonterminals

    def is_context_dependent(self, context):
        """Check if the grammar rule is context-dependent."""
        terminals, nonterminals = context
        return (
            len(self._output_symbols) >= len(self._input_symbols) and
            set(self._input_symbols) <= terminals | nonterminals and
            set(self._output_symbols) <= terminals | nonterminals | {EMPTY_SEQUNCE}
        )

    @staticmethod
    def parse(rule_string):
        """Parse grammar rule"""
        left_part, right_part = rule_string.split(sep='->')
        right_parts = right_part.split(sep='|')
        return [Rule(left_part, right_part) for right_part in right_parts]
