#!/usr/bin/python3
from itertools import chain
from collections import namedtuple
from enum import Enum
from utils.grammar_defenitions import Rule, EMPTY_SEQUNCE, GrammarType
from utils.rule import Rule


EMPTY_SEQUNCE = 'ε'


class GrammarType(Enum):
    '''Contains all possible grammar types.'''
    ZERO = 'Zero type grammar'
    CONTEXT_DEPENDENT = 'Context-dependent grammar'
    CONTEXT_FREE = 'Context-free grammar'
    REGULAR = 'Regular grammar'


class Grammar:
    def __init__(self, terminals, nonterminals, rules, start_symbol):
        self._terminals = terminals
        self._nonterminals = nonterminals
        self._rules = set(chain.from_iterable(Rule.parse(rule) for rule in rules))
        self._start_symbol = start_symbol

        validation_summary = self._validate_grammar(terminals, nonterminals, self._rules, start_symbol)
        if len(validation_summary):
            raise ValueError("\n".join(validation_summary))

    @property
    def grammar_type(self):
        """Identify type of the given grammar. All args are iterables of strings."""
        rule_context = (self._terminals, self._nonterminals)

        if all(rule.is_regular(rule_context) for rule in self._rules):
            return GrammarType.REGULAR
        elif all(rule.is_context_free(rule_context) for rule in self._rules):
            return GrammarType.CONTEXT_FREE
        elif all(rule.is_context_dependent(rule_context) for rule in self._rules):
            return GrammarType.CONTEXT_DEPENDENT
        return GrammarType.ZERO

    @staticmethod
    def get_grammar(data):
        terminals = set(data["terminals"])
        nonterminals = set(data["nonterminals"])
        rules = set(data["rules"])
        start_symbol = data["start_symbol"]
        return Grammar(terminals, nonterminals, rules, start_symbol)

    def _validate_grammar(self, terminals, nonterminals, rules, start_symbol):
        """Validate grammar rule"""
        validation_summary = []

        if not terminals - {EMPTY_SEQUNCE}:
            validation_summary.append("No terminals specified.")

        if not nonterminals - {EMPTY_SEQUNCE}:
            validation_summary.append("No non-terminals specified.")

        common = terminals & nonterminals
        if common:
            validation_summary.append(f"Terminals and nonterminals have common members: {common}.")

        if start_symbol not in nonterminals:
            validation_summary.append(f"Start symbol {start_symbol} is not in nonterminals {nonterminals}.")

        if not rules:
            validation_summary.append("No rules specified.")

        symbols_in_rules = set(chain.from_iterable(rule.input_symbols + rule.output_symbols for rule in rules))
        extra_symbols = (symbols_in_rules - (terminals | nonterminals | {EMPTY_SEQUNCE}))
        if extra_symbols:
            validation_summary.append(f"Your rules contain symbols that were not specified: {extra_symbols}.")

        return validation_summary
