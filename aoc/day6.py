def parse_map(lines):
    h = len(lines)
    w = len(lines[0])
    walls = {(r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "#"}
    start = next(
        (r, c) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "^"
    )

    return h, w, walls, start


# map of direction to new direction after turning at a wall
TURN_MAP = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}


def handle_walls(r, c, dr, dc, walls):
    while (r + dr, c + dc) in walls:
        dr, dc = TURN_MAP[dr, dc]
    return dr, dc


def part1(lines):
    w, h, walls, (r, c) = parse_map(lines)

    # up initially
    dr, dc = -1, 0

    visited = set()

    while 0 <= r < h and 0 <= c < w:
        visited.add((r, c))

        dr, dc = handle_walls(r, c, dr, dc, walls)

        r += dr
        c += dc

    return len(visited)


def part2(lines):
    w, h, walls, (r, c) = parse_map(lines)

    # up initially
    dr, dc = -1, 0

    # set of positions we've already considered (or disqualified) for a new wall
    considered = {(r, c)}

    visited = set()
    count = 0

    def is_loop(visited, r, c, dir_, walls):
        dr, dc = dir_
        visited = set(visited)  # copy so we don't pollute the source
        while 0 <= r < h and 0 <= c < w:
            # if we've been here while facing the same direction already, this is a loop
            if (r, c, dr, dc) in visited:
                return True

            visited.add((r, c, dr, dc))
            dr, dc = handle_walls(r, c, dr, dc, walls)

            r += dr
            c += dc

        return False

    while 0 <= r < h and 0 <= c < w:
        visited.add((r, c, dr, dc))
        dr, dc = handle_walls(r, c, dr, dc, walls)

        # consider a new wall directly ahead of us
        new_wall = (r + dr, c + dc)

        if new_wall not in considered and is_loop(
            visited, r, c, TURN_MAP[dr, dc], walls | {new_wall}
        ):
            count += 1

        considered.add(new_wall)

        r += dr
        c += dc

    return count
