from itertools import product


def part1(lines):
    h = len(lines)
    w = len(lines[0])

    pattern = list("XMAS")

    def match(r, c, dr, dc):
        # explicitly bail if out of bounds to avoid wrapping around with negative indices
        if not (0 <= r + 3 * dr < h and 0 <= c + 3 * dc < w):
            return False

        return [lines[r + i * dr][c + i * dc] for i in range(4)] == pattern

    return sum(
        match(r, c, dr, dc) for r, c, dr, dc in product(range(h), range(w), (-1, 0, 1), (-1, 0, 1))
    )


def part2(lines):
    h = len(lines)
    w = len(lines[0])

    # possible locations of "M" relative to the center "A"
    m_orientations = [
        {(-1, -1), (-1, 1)},
        {(-1, 1), (1, 1)},
        {(1, 1), (1, -1)},
        {(1, -1), (-1, -1)},
    ]

    def match(r, c, m_orientation):
        return lines[r][c] == "A" and all(
            lines[r + dr][c + dc] == ("M" if (dr, dc) in m_orientation else "S")
            for dr, dc in product((-1, 1), repeat=2)
        )

    return sum(
        match(r, c, m_orientation)
        for r, c, m_orientation in product(range(1, h - 1), range(1, w - 1), m_orientations)
    )
