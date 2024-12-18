from collections import deque


SIZE = 71


def parse(lines):
    return [tuple(int(x) for x in line.split(",")) for line in lines]


def run(walls):
    """BFS algorithm."""
    walls = set(walls)
    start = (0, 0)
    end = (SIZE - 1, SIZE - 1)

    visited = set()

    # FIFO queue of (position, distance) elements
    queue = deque([(start, 0)])

    while queue:
        (r, c), dist = queue.pop()

        if (r, c) in visited:
            continue

        if (r, c) == end:
            return dist

        visited.add((r, c))

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < SIZE and 0 <= c + dc < SIZE and (r + dr, c + dc) not in walls:
                queue.appendleft(((r + dr, c + dc), dist + 1))


def part1(lines):
    return run(parse(lines)[:1024])


def part2(lines):
    walls = parse(lines)

    # bisection algorithm to find the first byte which blocks the goal completely
    # min_ is a lower bound on the index of the last byte which does not block the goal
    # max_ is an upper bound on the index of the first byte which blocks the goal
    min_ = 0
    max_ = len(walls)

    while max_ - min_ > 1:
        trial = (max_ - min_) // 2 + min_
        result = run(walls[: trial + 1])
        if result is None:  # blocked
            max_ = trial
        else:
            min_ = trial

    # once max_ = min_ + 1, max_ will be the index of the first byte which blocks the goal
    return ",".join(str(x) for x in walls[max_])
