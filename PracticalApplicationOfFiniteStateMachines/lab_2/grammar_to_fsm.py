#!/usr/bin/env python3
'''Lab 2.
1. ввод произвольной формальной грамматики с клавиатуры и проверка
ее на принадлежность к классу регулярных грамматик;
2. построение по заданной регулярной грамматике конечного автомата;
3. преобразование недетерминированного конечного автомата к детерми-
нированному конечному автомату;
4. вывод графа результирующего конечного автомата на экран.
'''
import argparse
import random
import json
from collections import namedtuple
from itertools import product
from string import ascii_uppercase

import networkx as nx
from networkx.drawing.nx_pydot import to_pydot

from utils import (
    Grammar, GrammarError, Rule, EMPTY_SEQUENCE,
    terminal, nonterminal, get_term_nonterm,
)

# pylint: disable=line-too-long

GRAPH_STYLE = {
    'shape': 'hexagon',
    'style': 'rounded, filled',
    'color': 'cadetblue',
}


FSM = namedtuple('FSM', 'states, input_symbols, transitions, start_state, final_states')
Transition = namedtuple('Transition', 'state input_symbol new_state')


def add_new_rule(grammar: Grammar):
    '''Пополнить грамматику правилом A → aN , где A ∈ V N , a ∈ V T и
    N - новый нетерминал, для каждого правила вида A → a , если в грамматике нет
    соответствующего ему правила A → aB , где B ∈ V N .'''
    rules_with_terms = {
        rule for rule in grammar.rules
        if rule.right_part != EMPTY_SEQUENCE and
        set(rule.right_part) <= grammar.terminals
    }
    rules_without_other_nonterms = {
        rule for rule in grammar.rules
        if len(rule.right_part) == 2 and
        rule.left_part in rule.right_part
    }
    rules = rules_with_terms - {
        Rule(rule.left_part, get_term_nonterm(rule, grammar.terminals)[0])
        for rule in rules_without_other_nonterms
    }
    if rules:
        new_nonterm = ('N' if 'N' not in grammar.nonterminals
                       else random.choice(list(set(ascii_uppercase) - grammar.nonterminals)))
        grammar.nonterminals.add(new_nonterm)

        new_rules = {Rule(rule.left_part, rule.right_part + new_nonterm) for rule in rules}
        grammar.rules.update(new_rules)


def transform_rules_to_transitions(grammar):
    '''Каждое правило A → aB преобразовать в функцию переходов
    F ( A , a ) = B , где A , B ∈ V N , a ∈ V T .'''
    return {
        Transition(rule.left_part, *get_term_nonterm(rule, grammar.terminals))
        for rule in grammar.rules if len(rule.right_part) == 2
    }


def is_dfsm(fsm):
    '''Является ли КА ДКА?'''
    for state, symbol in product(fsm.states, fsm.input_symbols):
        new_states = {
            transition.new_state for transition in fsm.transitions
            if transition.state == state and transition.input_symbol == symbol
        }
        if len(new_states) > 1:
            return False
    return True


def introduce_new_states(fsm):
    substitutions = {}
    for states in fsm.states:
        if len(states) > 1:
            free_letters = set(ascii_uppercase) - fsm.states - set(substitutions.values())
            new_state = list(sorted(free_letters))[0]
            substitutions[states] = new_state
        elif len(states) == 1:
            state = list(states)[0]
            substitutions[frozenset(state)] = state

    states = {substitutions.get(state, state) for state in fsm.states if state}
    transitions = {
        Transition(substitutions.get(t.state, t.state),
                   t.input_symbol,
                   substitutions.get(t.new_state, t.new_state))
        for t in fsm.transitions if t.state and t.new_state
    }
    final_states = {substitutions.get(state, state) for state in fsm.final_states if state}
    return FSM(states, fsm.input_symbols, transitions, fsm.start_state, final_states)


def transform_nfsm_to_dfsm(fsm):
    dfsm = FSM(fsm.states, fsm.input_symbols, set(), fsm.start_state, set())
    queue = [frozenset(dfsm.start_state)]
    while queue:
        states = queue.pop()
        for symbol in dfsm.input_symbols:
            result_states = frozenset()
            for state in states:
                result_states |= frozenset(t.new_state for t in fsm.transitions
                                           if t.state == state and t.input_symbol == symbol)
            dfsm.transitions.add(Transition(states, symbol, result_states))
            if result_states not in dfsm.states:
                queue.append(result_states)
                dfsm.states.add(result_states)
    final_states = {state for state in fsm.final_states if state in dfsm.states}
    dfsm.final_states.update(final_states)
    return introduce_new_states(dfsm)


def make_finite_state_machine(grammar: Grammar):
    '''Преобразовать регулярную грамматику в конечный автомат'''
    add_new_rule(grammar)

    # Начальный символ грамматики S принять за начальное состояние КА H.
    start_state = grammar.start_symbol
    # Из нетерминалов образовать множество состояний автомата Q = V N ∪ {N },
    states = grammar.nonterminals
    # а из терминалов – множество символов входного алфавита T = V T .
    input_symbols = grammar.terminals

    transitions = transform_rules_to_transitions(grammar)

    # Если в грамматике имеется правило S → ε , где S - начальный символ грамматики,
    # то поместить S во множество заключительных состояний.
    final_states = {
        grammar.start_symbol
    } if Rule(grammar.start_symbol, EMPTY_SEQUENCE) in grammar.rules else set()

    fsm = FSM(states, input_symbols, transitions, start_state, final_states)

    # Если получен НКА, то преобразовать его в ДКА
    if not is_dfsm(fsm):
        fsm = transform_nfsm_to_dfsm(fsm)
    return fsm


def visualize_fsm(fsm):
    '''Draw an image of fsm graph.'''
    graph = nx.DiGraph()
    graph.add_edges_from((t.state, t.new_state, {'label': t.input_symbol}) for t in fsm.transitions)
    for node in graph.nodes().values():
        node.update(GRAPH_STYLE)
    pydot_graph = to_pydot(graph)
    with open('lab2.png', 'wb') as image_file:
        image_file.write(pydot_graph.create_png())


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Grammar recognition.",
        prog="gr")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="grammar.json",
        help="JSON file with grammar")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.5")

    return parser.parse_args()


def _get_grammar(grammar_data):
    terminals = list(grammar_data["terminals"])
    nonterminals = list(grammar_data["nonterminals"])
    rules = grammar_data["rules"]
    start_symbol = grammar_data["start_symbol"]
    return Grammar(terminals, nonterminals, rules, start_symbol)


def main():
    args = _parse_arguments()
    try:
        with open(args.source) as json_file:
            grammar_data = json.load(json_file)
            grammar = _get_grammar(grammar_data)
            if not grammar.is_regular():
                raise GrammarError('Given grammar is not regular.')
            fsm = make_finite_state_machine(grammar)
            visualize_fsm(fsm)
    except GrammarError as error:
        arg_parser.error(str(error))


if __name__ == '__main__':
    main()
