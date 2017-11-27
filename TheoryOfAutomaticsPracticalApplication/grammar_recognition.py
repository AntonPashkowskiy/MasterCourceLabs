#!/usr/bin/python3
import argparse
import json
from itertools import chain
from utils.grammar import Grammar


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Grammar recognition.",
        prog="tvs")
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
        grammar = Grammar.get_grammar(grammar_data)
        print(grammar.grammar_type.value)


if __name__ == "__main__":
    main()
