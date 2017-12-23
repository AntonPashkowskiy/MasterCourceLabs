#!/usr/bin/python3
import re
import networkx as nx
from collections import defaultdict
from networkx.drawing.nx_pydot import to_pydot


class OptimizingFiniteStateMachine:
    GRAPH_STYLE = {
        'shape': 'hexagon',
        'style': 'rounded, filled',
        'color': 'cadetblue',
    }
    FORMAT = re.compile(r"""
        automata\n
            [ ]*states[ ](?P<states>[^\n]+)\n
            [ ]*start[ ](?P<start>[^\n]+)\n
            [ ]*input_symbols[ ](?P<input_symbols>[^\n]+)\n
            (?P<rules>([ ]*rule[ ][^\n]+\n)+)
        end
    """, re.X)
    RULE_FORMAT = re.compile(r'rule (?P<cur>.+) (?P<input>.+) (?P<next>.+)')
    EXIT_STATE = 'EXIT_STATE'
    ERROR_STATE = 'ERROR_STATE'

    def __init__(self, states, input_symbols, start_state, transition_rules):
        self.states = set(states)
        self.start_state = start_state
        self.exit_state = {OptimizingFiniteStateMachine.EXIT_STATE}
        self.input_symbols = input_symbols
        self.transition_rules = transition_rules

    def __str__(self):
        template = 'Automata:\n  States: {}\n  Start state: {}\n  Rules: {}\n'
        rules = ''
        for key, val in self.transition_rules.items():
            rules += '\n    ' + str(key) + ' => ' + str(val)
        return template.format(self.states, self.start_state, rules)

    def __iter__(self):
        return iter([
            self.states,
            self.start_state,
            self.input_symbols,
            self.transition_rules
        ])

    @staticmethod
    def from_file(filename):
        """Reading and parsing fsm from file"""
        with open(filename, 'r') as fsm_file:
            fsm_description = fsm_file.read()

        parsed_description = re.match(OptimizingFiniteStateMachine.FORMAT, fsm_description)
        if not parsed_description:
            raise ValueError("Error in description of fsm.")

        states = parsed_description.group('states').split()
        start_state = parsed_description.group('start').split()
        input_symbols = parsed_description.group('input_symbols').split()
        rules_description = parsed_description.group('rules').split('\n')
        transition_rules = defaultdict(frozenset)

        for rule in rules_description:
            rule_description = re.match(OptimizingFiniteStateMachine.RULE_FORMAT, rule.strip())
            if not rule_description:
                continue
            current_state = frozenset(rule_description.group('cur'))
            input_symbol = rule_description.group('input')
            next_state = frozenset(rule_description.group('next'))
            transition_rules[(current_state, input_symbol)] |= next_state

        return OptimizingFiniteStateMachine(
            states=[frozenset(state) for state in states],
            input_symbols=input_symbols,
            start_state=frozenset(start_state),
            transition_rules=transition_rules
        )

    def exclude_unreachable_states(self):
        states, start_state, input_symbols, transitions = self
        visited_states = {start_state}
        visited_states_changed = True

        while visited_states_changed:
            new_visited_states = visited_states.copy()
            for input_symbol in input_symbols:
                next_states = self._get_next_states(visited_states, input_symbol, True)
                if not next_states:
                    continue
                if len(next_states) > 1:
                    next_states = {frozenset(s) for s in next_states}
                else:
                    next_states = {next_states}
                new_visited_states = new_visited_states.union(next_states)
            visited_states_changed = new_visited_states != visited_states
            visited_states = new_visited_states.copy()

        unreachable_states = states - visited_states
        new_transitions = defaultdict(frozenset)
        for (state, input_symbol), next_state in transitions.items():
            if state in unreachable_states:
                continue
            new_transitions[(state, input_symbol)] |= next_state

        return OptimizingFiniteStateMachine(
            states=visited_states,
            start_state=start_state,
            input_symbols=input_symbols,
            transition_rules=new_transitions
        )

    def exclude_equivalent_states(self, final_states):
        states, start_state, input_symbols, transitions = self
        states = frozenset(states)
        partitions = {states - final_states, final_states}
        queue = {final_states}

        while queue:
            qpart = queue.pop()
            qpart_ancestors = set()
            # Find all states which have transtions to qpart
            for input_symbol in input_symbols:
                for (state, symbol), next_state in transitions.items():
                    if input_symbol == symbol and next_state in qpart:
                        qpart_ancestors.add(state)
            # Create new partitions
            qpart = qpart_ancestors
            new_partitions = partitions.copy()
            for states_set in partitions:
                intersect = states_set.intersection(qpart)
                difference = states_set - qpart
                new_partitions.remove(states_set)
                new_partitions.add(intersect)
                new_partitions.add(difference)
                if not intersect or not difference:
                    continue
                # While unable to partitioning last state set
                if states_set in queue:
                    queue.remove(states_set)
                    queue.add(intersect)
                    queue.add(difference)
                else:
                    queue.add(
                        intersect if len(intersect) <= len(difference) else difference
                    )
            partitions = new_partitions.copy()

        # Create set of partitions
        partitions = {
            frozenset(list(state)[0] for state in states_set) for states_set in partitions if states_set
        }

        old_to_new_state_mapping = {}
        for states_set in partitions:
            for state in states_set:
                old_to_new_state_mapping[frozenset({state})] = states_set

        new_transitions = defaultdict(frozenset)
        for (state, symbol), new_state in transitions.items():
            new_transitions[old_to_new_state_mapping[state], symbol] = old_to_new_state_mapping[new_state]

        return OptimizingFiniteStateMachine(
            states=partitions,
            start_state=start_state,
            input_symbols=input_symbols,
            transition_rules=new_transitions
        )

    def save_in_file(self, filename):
        """Save fsm graph as image"""
        graph = nx.DiGraph()
        graph.add_edges_from((state, new_state, {'label': symbol}) for state, symbol, new_state in self._get_transition_rules())
        for node in graph.nodes().values():
            node.update(OptimizingFiniteStateMachine.GRAPH_STYLE)

        pydot_graph = to_pydot(graph)
        with open(filename, 'wb') as image_file:
            image_file.write(pydot_graph.create_png())

    def _get_next_states(self, current_states, input_symbol, no_errors=False):
        next_states = frozenset()
        error = frozenset({self.ERROR_STATE})
        for state in current_states:
            next_state = self.transition_rules.get(
                (state, input_symbol), error
            )
            if no_errors and next_state == error:
                continue
            next_states |= next_state
        return next_states

    def _get_transition_rules(self):
        def to_label(state):
            return ' '.join(list(state))

        transitions = {}
        for (state, symbol), new_state in self.transition_rules.items():
            key = (to_label(state), to_label(new_state))
            if key not in transitions:
                transitions[key] = symbol
            else:
                transitions[key] = " ".join([transitions[key], symbol])

        for key in transitions:
            state, new_state = key
            yield state, transitions[key], new_state


if __name__ == '__main__':
    dfsm = OptimizingFiniteStateMachine.from_file("input_fsm.txt")
    min_dfsm = dfsm.exclude_unreachable_states()\
        .exclude_equivalent_states(final_states=frozenset({frozenset('I')}))

    dfsm.save_in_file("dfsm.png")
    min_dfsm.save_in_file("min_dfsm.png")
