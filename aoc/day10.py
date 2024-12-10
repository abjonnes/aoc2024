from collections import defaultdict
from itertools import product


def run(lines, summit_transform):
    lines = [[int(x) for x in line] for line in lines]

    h = len(lines)
    w = len(lines[0])

    # mapping of positions at a certain height to which summits are reachable via a "good" trail;
    # repeated summits in the list represent different paths to that summit
    reachable = defaultdict(list)

    # initially populate with the summits themselves (height 9)
    reachable.update(
        {
            (r, c): [(r, c)]
            for r, line in enumerate(lines)
            for c, char in enumerate(line)
            if char == 9
        }
    )

    # iterate, decreasing in height by one step until we reach the bottom
    for height in reversed(range(9)):
        # every iteration, replace the structure with data only for the height of interest so that
        # at the end, we have data only for the trailheads
        new_reachable = defaultdict(list)

        for r, c in product(range(h), range(w)):
            # if not the height of interest for this iteration, skip
            if lines[r][c] != height:
                continue

            # consider each neighbor
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                # if out of bounds or not path of a "good" trail, skip
                if not (0 <= r + dr < h and 0 <= c + dc < w) or lines[r + dr][c + dc] != height + 1:
                    continue

                # add the reachable summits to this position
                new_reachable[r, c].extend(reachable[r + dr, c + dc])

        reachable = new_reachable

    return sum(len(summit_transform(summits)) for summits in reachable.values())


def part1(lines):
    # `set` will uniquify the reachable summits to give the trailhead's score
    return run(lines, set)


def part2(lines):
    # `list` (essentially a no-op transform) to give the trailhead's rating
    return run(lines, list)
