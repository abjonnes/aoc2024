import heapq


def parse(lines):
    tiles = set()
    start = None
    end = None
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == ".":
                tiles.add((r, c))
            if char == "S":
                start = r, c
            if char == "E":
                end = r, c

    assert start
    assert end

    tiles.add(start)
    tiles.add(end)

    return tiles, start, end


def run(lines):
    tiles, start, end = parse(lines)

    # use a min-queue (heap) with (score, position, heading, history)
    # history stores a set of nodes encountered on paths which led to this position
    queue = [(0, start, (0, 1), set())]

    visited = set()

    last_score = None
    last_pos = None
    last_history = None  # pointer to the previous history object in memory
    while queue:
        score, (r, c), heading, history = heapq.heappop(queue)

        # merge histories if two paths converge at the same location with the same score
        if last_score == score and last_pos == (r, c) and last_history:
            last_history.update(history)

        # if we've been here with the same heading, don't continue (redundant)
        if ((r, c), heading) in visited:
            continue

        visited.add(((r, c), heading))
        # this creates a _copy_ of the history object with the current location, so that we don't
        # update the other paths' history objects
        history = history | {(r, c)}

        # success!
        if (r, c) == end:
            return score, len(history)

        # consider the neighboring directions
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_r = r + dr
            new_c = c + dc

            # check for the wall and prevent a 180 degree turn
            if (new_r, new_c) not in tiles or (new_r, new_c) == last_pos:
                continue

            # otherwise add new locations and scores to the queue
            heapq.heappush(
                queue,
                (score + (1 if (dr, dc) == heading else 1001), (new_r, new_c), (dr, dc), history),
            )

        last_score = score
        last_history = history
        last_pos = r, c


def part1(lines):
    score, _ = run(lines)
    return score


def part2(lines):
    _, n_nodes = run(lines)
    return n_nodes
