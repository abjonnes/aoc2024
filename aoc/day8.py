from collections import defaultdict
from itertools import permutations, takewhile


def parse(lines):
    """Return a dictionary of antenna type to list of locations."""
    antennae = defaultdict(list)
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == ".":
                continue
            antennae[char].append((r, c))

    return antennae


def run(lines, pos_generator):
    """`pos_generator` is a generator which yields potential antinode locations given two antenna
    positions as input. It may generate locations which are out of bounds, and it may generate
    infinite locations, as long as the locations are generated in distance order.
    """
    antennae = parse(lines)

    h = len(lines)
    w = len(lines[0])

    def in_bounds(pos):
        r, c = pos
        return 0 <= r < h and 0 <= c < w

    locations = set()
    for positions in antennae.values():
        # permutations here rather than combinations so each call only needs to generate locations
        # in a single direction
        for pos1, pos2 in permutations(positions, r=2):
            locations.update(takewhile(in_bounds, pos_generator(pos1, pos2)))

    return len(locations)


def part1(lines):
    def pos_generator(pos1, pos2):
        """Yield a single position which is the nearest to `pos2` along the `pos1`-`pos2` axis."""
        r1, c1 = pos1
        r2, c2 = pos2

        dr = r2 - r1
        dc = c2 - c1

        yield r2 + dr, c2 + dc

    return run(lines, pos_generator)


def part2(lines):
    def pos_generator(pos1, pos2):
        """Infinitely yield positions along the `pos1`-`pos2` axis, starting with `pos2` and moving
        outward. (The positions along the axis in the other direction will be yielded by a call to
        this generator with `pos1` and `pos2` reversed.)
        """
        r1, c1 = pos1
        r2, c2 = pos2

        dr = r2 - r1
        dc = c2 - c1

        while True:
            yield r2, c2
            r2 += dr
            c2 += dc

    return run(lines, pos_generator)
