from collections import defaultdict
from itertools import count, product


def parse(lines):
    maze = {
        (r, c)
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if char in (".", "S", "E")
    }
    start = next(
        (r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "S"
    )
    end = next((r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "E")

    return maze, start, end


def run(lines, cheat_radius):
    maze, start, end = parse(lines)

    # generate a set of relative positions reachable within the allowed radius, along with their
    # distances
    cheat_rel_positions = {
        ((dr, dc), dist)
        for dr, dc in product(range(-cheat_radius, cheat_radius + 1), repeat=2)
        if (dist := abs(dr) + abs(dc)) <= cheat_radius and (dr or dc)
    }

    # keys are source positions, values are mappings from cheat-reachable positions to the number of
    # steps required to reach
    cheatable = defaultdict(dict)

    # set of cheats we've identified so far
    found_cheats = set()

    r, c = start
    last = next_ = None

    for step in count():
        # determine which, if any, cheats get us here and save us >= 100 steps
        found_cheats.update(
            (source, (r, c)) for source, value in cheatable[r, c].items() if step - value >= 100
        )

        if (r, c) == end:
            break

        # find the next position
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (r + dr, c + dc) in maze and (r + dr, c + dc) != last:
                next_ = r + dr, c + dc

        # update which positions are reachable from here if we cheat
        for (dr, dc), dist in cheat_rel_positions:
            if (r + dr, c + dc) in maze:
                cheatable[r + dr, c + dc][r, c] = step + dist

        last = r, c

        assert next_
        r, c = next_

    return len(found_cheats)


def part1(lines):
    return run(lines, 2)


def part2(lines):
    return run(lines, 20)
