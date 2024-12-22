from collections import Counter, defaultdict
from itertools import pairwise, product


def calculate_moves(source, dest, hole_row):
    """For given source and destination key coordinates, return an ordered list of directional key
    pairs which move the robot across the keypad from source to destination. When the robot needs to
    be moved from key to key, the traversal represented by the returned key pairs are the movements
    that the operating robot (or human) must complete to move the robot. The key pair representation
    admits an iterative solution, as the operating robot's movements returned at this level become
    the movements that the next level of robot will need to perform, and so on.

    The specific order of movements returned here results in the fewest operations required, as
    determined by inspection of level 4 and higher.
    """
    r1, c1 = source
    r2, c2 = dest

    updown = ("^" if r2 < r1 else "v") * abs(r2 - r1)
    leftright = ("<" if c2 < c1 else ">") * abs(c2 - c1)

    # first two conditions are to avoid passing over the empty spaces
    if r1 == hole_row and c2 == 0:
        value = updown + leftright
    elif r2 == hole_row and c1 == 0 or c2 < c1:
        value = leftright + updown
    # if no danger of crossing empty space, move horizontally first only if we're moving left
    elif c2 < c1:
        value = leftright + updown
    # otherwise, move vertically first
    else:
        value = updown + leftright

    # include movements to and from the "A" key
    return list(pairwise(f"A{value}A"))


# for the two keypads, calculate the full matrix of movements required to go from any source key to
# any destination key
NUM_POS = {str(i): ((9 - i) // 3, (i + 2) % 3) for i in range(1, 10)}
NUM_POS["0"] = (3, 1)
NUM_POS["A"] = (3, 2)
NUM_SHIFTS = {
    (n1, n2): calculate_moves(source, dest, 3)
    for (n1, source), (n2, dest) in product(NUM_POS.items(), repeat=2)
}

DIR_POS = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}
DIR_SHIFTS = {
    (n1, n2): calculate_moves(source, dest, 0)
    for (n1, source), (n2, dest) in product(DIR_POS.items(), repeat=2)
}


def transform(counts, shifts):
    """Given transitions and their counts, calculate the required transitions for the next level of
    robot. The ordering of the transitions does not impact the results, so we can simply store the
    counts.
    """
    new_counts = defaultdict(int)
    for source_pair, count in counts.items():
        for pair in shifts[source_pair]:
            new_counts[pair] += count
    return new_counts


def run(lines, n_dir_robots):
    for value in lines:
        counts = Counter(pairwise("A" + value))
        counts = transform(counts, NUM_SHIFTS)
        for _ in range(n_dir_robots):
            counts = transform(counts, DIR_SHIFTS)
        yield int(value[:-1]) * sum(counts.values())


def part1(lines):
    return sum(run(lines, 2))


def part2(lines):
    return sum(run(lines, 25))
