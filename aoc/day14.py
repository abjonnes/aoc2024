from collections import defaultdict
from itertools import count
from math import prod
import re
from time import sleep

from egcd import egcd


HEIGHT = 103
WIDTH = 101


def parse(lines):
    return [[int(x) for x in re.findall(r"-?\d+", line)] for line in lines]


def part1(lines):
    def quadrant(x, y):
        """Return a quadrant identifier given coordinates. Identifiers are from (0, 1, 2, 3) but
        don't necessarily correspond to the familiar cartesian coordinate quadrants.
        """
        if x == WIDTH // 2 or y == HEIGHT // 2:
            return  # will ignore the None key later
        return (2 * int(x < WIDTH // 2)) + int(y < HEIGHT // 2)

    counts = defaultdict(int)

    for px, py, vx, vy in parse(lines):
        x = (px + 100 * vx) % WIDTH
        y = (py + 100 * vy) % HEIGHT
        counts[quadrant(x, y)] += 1

    return prod(counts[q] for q in range(4))


def part2(lines):
    def printit(time):
        occupied = {
            ((px + time * vx) % WIDTH, (py + time * vy) % HEIGHT) for px, py, vx, vy in parse(lines)
        }
        print(f"Time {time}")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                char = "*" if (x, y) in occupied else " "
                print(char, end="")
            print()

    # uncomment this to "watch" the movement over time
    # for time in count():
    #     printit(time)
    #     sleep(0.5)

    # from inspection, robots cluster along x dimension at time 93
    #                                       y dimension at time 72

    tx = 93
    ty = 72
    dt = tx - ty

    # m*WIDTH + n*HEIGHT = g
    g, m, n = egcd(WIDTH, HEIGHT)
    assert g == 1  # ensure width and height are coprime

    # dt*(m*WIDTH + n*HEIGHT) = dt = tx - ty
    # dt*n*HEIGHT + ty = -dt*m*WIDTH + tx

    # solve for t, where t is *a* (possibly negative) time at which the tree is visible:
    assert dt * n * HEIGHT + ty == -dt * m * WIDTH + tx  # validate the math
    t = dt * n * HEIGHT + ty

    # return the first such time
    return t % (WIDTH * HEIGHT)
