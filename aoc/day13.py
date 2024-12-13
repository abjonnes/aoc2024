import re


def parse(lines):
    def get_numbers(line):
        return [int(x) for x in re.findall(r"\d+", line)]

    it = iter(lines)
    try:
        while True:
            a, b, p = next(it), next(it), next(it)
            yield [get_numbers(x) for x in (a, b, p)]
            next(it)
    except StopIteration:
        pass


def run(lines, dp=0):
    """Change of basis algorithm."""
    sum_ = 0
    for (ax, ay), (bx, by), (px, py) in parse(lines):
        px += dp
        py += dp

        # find the determinant of the change-of-basis matrix
        det = ax * by - ay * bx

        # if determinant is 0, matrix is singular (A and B are multiples of each other), but this
        # doesn't happen in the input
        if not det:
            raise NotImplementedError("This doesn't seem to happen")

        # prize coordinates in the new basis (not yet scaled by determinant)
        a = by * px - bx * py
        b = ax * py - ay * px

        # if not integers or negative (after scaling), prize unreachable
        if a % det or b % det or det * a < 0 or det * b < 0:
            continue

        sum_ += (3 * a + b) // det

    return sum_


def part1(lines):
    return run(lines)


def part2(lines):
    return run(lines, 10000000000000)
