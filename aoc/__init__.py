from importlib import import_module
from inspect import signature
import os

import click
import requests


INPUT_URL = "https://adventofcode.com/2024/day/{day}/input"


def get_input(day):
    response = requests.get(
        INPUT_URL.format(day=day), cookies={"session": os.environ["AOC_SESSION"]}
    )
    response.raise_for_status()
    return response.text


def format_output(output):
    if isinstance(output, str) and "\n" in output:
        return "\n" + output
    return str(output)


def run_part(part, data):
    sig = signature(part)
    args = dict()
    if "data" in sig.parameters:
        args["data"] = data
    if "lines" in sig.parameters:
        lines = data.split("\n")

        # remove the line resulting from the last newline
        if not lines[-1]:
            lines.pop()

        args["lines"] = lines

    return part(**args)


@click.command()
@click.argument("day", type=int, required=True)
def aoc(day):
    module = import_module(f"aoc.day{day}")

    data = get_input(day)

    try:
        print(f"Part 1: {format_output(run_part(module.part1, data))}")

        if hasattr(module, "part2"):
            print(f"Part 2: {format_output(run_part(module.part2, data))}")
    except KeyboardInterrupt:
        import traceback, sys

        traceback.print_exc(file=sys.stdout)
