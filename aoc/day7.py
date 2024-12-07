from itertools import product
import operator

def parse(lines):
    for line in lines:
        target, rest = line.split(":")
        inputs = rest.split()
        yield int(target), [int(x) for x in inputs]

def run(lines, *operations):

    def is_valid(target, inputs):
        start = inputs.pop(0)
        for ops in product(operations, repeat=len(inputs)):
            value = start

            for op, operand in zip(ops, inputs):
                value = op(value, operand)

            if value == target:
                return True

    return sum(target for target, inputs in parse(lines) if is_valid(target, inputs))


def part1(lines):
    return run(lines, operator.add, operator.mul)

def part2(lines):
    def concat(x, y):
        return int(str(x) + str(y))

    return run(lines, operator.add, operator.mul, concat)
