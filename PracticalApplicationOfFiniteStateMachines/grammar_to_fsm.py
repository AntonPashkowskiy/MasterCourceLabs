#!/usr/bin/python3
import argparse
import json
import os
from itertools import chain
from utils.grammar import Grammar, GrammarType
from utils.fsm import FiniteStateMachine


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Grammar to finite state machine transform.",
        prog="gtf")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="grammar.json",
        help="JSON file with grammar")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.5")

    return parser.parse_args()


def _save_image(image, filename="result_graph.png"):
    with open(filename, "wb") as image_file:
        image_file.write(image)


def main():
    args = _parse_arguments()
    with open(args.source) as json_file:
        grammar_data = json.load(json_file)
        try:
            grammar = Grammar.get_grammar(grammar_data)
            if grammar.grammar_type is not GrammarType.REGULAR:
                raise ValueError("Grammar is not regular.")
            determined_fsm = FiniteStateMachine.get_determined_from_grammar(grammar)
            determined_fsm_graph = determined_fsm.to_graph_image()
            _save_image(determined_fsm_graph)
        except ValueError error:
            print(error)


if __name__ == "__main__":
    main()
