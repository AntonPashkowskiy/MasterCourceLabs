'''Contains code shared between multiple labs.'''
from collections import namedtuple, Iterable
from itertools import chain
from enum import Enum


DERIVIABILITY_SIGN = '->'
SEQUENCE_SEPARATOR = '|'
EMPTY_SEQUENCE = 'ε'


Rule = namedtuple('Rule', 'left_part, right_part')


class GrammarError(ValueError):
    '''Custom exception type for errors conected with grammars.'''


class GrammarType(Enum):
    '''Contains all possible grammar types.'''
    ZERO = 'zero'
    CONTEXT_DEPENDENT = 'context-dependent'
    CONTEXT_FREE = 'context-free'
    REGULAR = 'regular'


def symbol_type(symbol_string: str) -> str:
    '''Symbol argument type used by argparse.'''
    if len(symbol_string) > 1:
        raise ValueError('Symbols can only be represented with exactly 1 character.')
    # if not symbol_string.isalnum():
    #     raise ValueError('Symbols can only be represented with alphanumeric character.')
    return symbol_string


def terminal(symbol_string: str) -> str:
    '''Terminal symbol argument type used by argparse.'''
    symbol = symbol_type(symbol_string)
    if symbol.isupper():
        raise ValueError('Terminals can only be represented with lowercase letters and digits.')
    return symbol


def nonterminal(symbol_string: str) -> str:
    '''Nonterminal symbol argument type used by argparse.'''
    symbol = symbol_type(symbol_string)
    if not symbol.isupper():
        raise ValueError('Nonterminals can only be represented with uppercase letters.')
    return symbol


class Grammar:
    '''Represents formal grammar.'''
    def __init__(self, terminals: Iterable, nonterminals: Iterable, rules: Iterable, start_symbol: str):
        self.terminals = set(terminals)
        self.nonterminals = set(nonterminals)
        if not self.terminals.isdisjoint(self.nonterminals):
            raise GrammarError("Nonterminals' and terminals' sets mustn't overlap.")
        self.symbols = self.terminals | self.nonterminals | {EMPTY_SEQUENCE}
        self.start_symbol = start_symbol
        if self.start_symbol not in self.nonterminals:
            raise GrammarError("Start symbol should be a nonterminal.")
        self.rules = self._tune_rules(rules)

    def _tune_rules(self, rules: Iterable) -> set:
        def _parse_rule(rule: str) -> set:
            left_part, right_parts = rule.split(sep=DERIVIABILITY_SIGN)
            right_parts = right_parts.split(sep=SEQUENCE_SEPARATOR)
            return {Rule(left_part, right_part) for right_part in right_parts}

        tuned_rules = set()
        for rule in rules:
            tuned_rules |= _parse_rule(rule)
        for seq in chain.from_iterable(tuned_rules):
            for symbol in seq:
                if symbol not in self.symbols:
                    raise GrammarError(f'Rule contains unknown symbol {symbol}: {seq}.')
        return tuned_rules

    def is_regular(self) -> bool:
        '''Check if grammar is regular.'''
        if all(is_regular(rule, self.terminals, self.nonterminals) for rule in self.rules):
            return True
        return False

    def is_context_free(self) -> bool:
        '''Check if grammar is context-free.'''
        if all(is_context_free(rule, self.terminals, self.nonterminals) for rule in self.rules):
            return True
        return False

    def is_context_dependent(self) -> bool:
        '''Check if grammar is context-dependent.'''
        if all(is_context_dependent(rule, self.terminals, self.nonterminals) for rule in self.rules):
            return True
        return False

    @property
    def type(self) -> GrammarType:
        '''Identify type of the given grammar.'''
        if self.is_regular():
            return GrammarType.REGULAR
        elif self.is_context_free():
            return GrammarType.CONTEXT_FREE
        elif self.is_context_dependent():
            return GrammarType.CONTEXT_DEPENDENT
        return GrammarType.ZERO


def is_regular(rule, terminals, nonterminals):
    '''Check if rule grammar is regular.'''
    return (
        is_context_free(rule, terminals, nonterminals) and
        (
            len(rule.right_part) == 2 and
            set(rule.right_part) & terminals and
            set(rule.right_part) & nonterminals
        ) or (
            len(rule.right_part) == 1 and
            set(rule.right_part) <= nonterminals | terminals | {EMPTY_SEQUENCE}
        )
    )


def is_context_free(rule, terminals, nonterminals):
    '''Check if the grammar rule is context-free.'''
    return len(rule.left_part) == 1 and rule.left_part in nonterminals


def is_context_dependent(rule, terminals, nonterminals):
    '''Check if the grammar rule is context-dependent.'''
    return (
        len(rule.right_part) >= len(rule.left_part) and
        set(rule.left_part) <= terminals | nonterminals and
        set(rule.right_part) <= terminals | nonterminals | {EMPTY_SEQUENCE}
    )


def get_term_nonterm(rule, terminals):
    '''Returns terminal and nonterminal symbols of the right part of a regular rule.'''
    return (
        (rule.right_part[0], rule.right_part[1])
        if rule.right_part[0] in terminals
        else (rule.right_part[1], rule.right_part[0])
    )
