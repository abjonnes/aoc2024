from itertools import product


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def run(lines, factor):
    visited = set()
    h = len(lines)
    w = len(lines[0])

    def fill(r, c):
        """Find all nodes within a region given a starting node."""
        type_ = lines[r][c]
        region = set()
        queue = {(r, c)}
        while queue:
            r, c = queue.pop()
            region.add((r, c))
            for dr, dc in DIRECTIONS:
                # candidate neighbor
                new_r = r + dr
                new_c = c + dc

                if (
                    0 <= new_r < h  # in bounds
                    and 0 <= new_c < w  # in bounds
                    and (new_r, new_c) not in region  # not already considered
                    and lines[new_r][new_c] == type_  # same type
                ):
                    queue.add((new_r, new_c))

        return region

    price = 0

    for r, c in product(range(h), range(w)):
        # if already considered as part of an earlier region, skip
        if (r, c) in visited:
            continue

        region = fill(r, c)
        visited.update(region)

        price += len(region) * factor(region)

    return price


def part1(lines):
    def perimeter(region):
        # if a neighbor is outside the region, this is a segment of the perimeter
        return sum(
            (r + dr, c + dc) not in region for (r, c), (dr, dc) in product(region, DIRECTIONS)
        )

    return run(lines, perimeter)


def part2(lines):
    def sides(region):
        def sides_1d(node_set):
            """Find the sides of the region in one dimension, i.e. horizontal or vertical sides."""
            # find bounding box
            min_x = min(x for x, _ in region)
            max_x = max(x for x, _ in region) + 1
            min_y = min(y for _, y in region)
            max_y = max(y for _, y in region) + 1

            count = 0
            side = False  # whether we're currently following along a side

            # scan over positions in the region in the direction of interest
            for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
                # if this node and the neighbor above it are either both in the region or both
                # outside, we're not or no longer following along a side
                if ((x, y) in node_set) == ((x - 1, y) in node_set):
                    # if we had been along a side up til now, we've identified a full side
                    if side:
                        count += 1
                    side = False
                    continue

                # at this point, we're along a side

                # edge case: if we were already along a side and only one of either this node or the
                # previous node were in the set, then we've hit an "intersection" of the fences
                # which counts as separate sides; see the middle of this example diagram
                # AAAAAA
                # AAA..A
                # AAA..A
                # A..AAA
                # A..AAA
                # AAAAAA
                if side and ((x, y) in node_set) != ((x, y - 1) in node_set):
                    count += 1

                side = True

            return count

        horizontal_sides = sides_1d(region)

        # transpose the grid
        region = {(c, r) for r, c in region}

        vertical_sides = sides_1d(region)

        return horizontal_sides + vertical_sides

    return run(lines, sides)
