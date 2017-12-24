#!/usr/bin/python3
import argparse
import json
from utils.grammar import Grammar, GrammarType
from utils.file_logger import FileLogger
from automatons.pushdown_automaton import PushdownAutomaton
from automatons.extended_pushdown_automaton import ExtendedPushdownAutomaton


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Grammar to pushdown automaton.",
        prog="gtpda")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="grammar.json",
        help="JSON file with grammar")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.5")

    return parser.parse_args()


def main():
    args = _parse_arguments()
    with open(args.source) as json_file:
        grammar_data = json.load(json_file)
        try:
            grammar = Grammar.get_grammar(grammar_data)
            if grammar.grammar_type != GrammarType.CONTEXT_FREE:
                raise ValueError("Grammar should be context free.")

            with FileLogger("pushdown_automaton_trace.txt") as logger:
                pd_automaton = PushdownAutomaton.from_grammar(grammar)
                pd_automaton.set_logger(logger)

                pd_automaton.set_input_sequence('$y$')
                print(pd_automaton.start())
                pd_automaton.set_input_sequence('xxxxx$y$')
                print(pd_automaton.start())
                pd_automaton.set_input_sequence('x#x#$z$y$')
                print(pd_automaton.start())

            with FileLogger("pushdown_automaton_ext_trace.txt") as logger:
                epd_automaton = ExtendedPushdownAutomaton.from_grammar(grammar)
                epd_automaton.set_logger(logger)

                epd_automaton.set_input_sequence('$y$')
                print(epd_automaton.start())
                epd_automaton.set_input_sequence('xxxxx$y$')
                print(epd_automaton.start())
                epd_automaton.set_input_sequence('x#x#$z$y$')
                print(epd_automaton.start())
        except ValueError as error:
            print(error)

 
if __name__ == "__main__":
    main()
