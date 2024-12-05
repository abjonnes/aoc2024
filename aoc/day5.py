from collections import defaultdict
from itertools import chain


def parse(lines):
    orderings = defaultdict(set)
    lines = iter(lines)

    for line in lines:
        if not line:
            break
        page1, page2 = [int(x) for x in line.split("|")]
        orderings[page2].add(page1)

    updates = [[int(x) for x in line.split(",")] for line in lines]

    def is_ordered(update):
        disallowed = set()
        for page in update:
            if page in disallowed:
                break
            disallowed.update(orderings[page])
        else:
            return True

        # if we get here, we broke from the loop above
        return False

    partitioned_updates = {True: list(), False: list()}

    for update in updates:
        partitioned_updates[is_ordered(update)].append(update)

    return orderings, partitioned_updates[True], partitioned_updates[False]


def part1(lines):
    _, good_updates, _ = parse(lines)

    return sum(update[len(update) // 2] for update in good_updates)


def part2(lines):
    orderings, _, bad_updates = parse(lines)

    def reorder(update):
        pages = set(update)
        new_update = list()

        while pages:
            disallowed = set().union(chain.from_iterable(orderings[page] for page in pages))
            next_page = (pages - disallowed).pop()
            pages.remove(next_page)
            new_update.append(next_page)

        return new_update

    return sum(reorder(update)[len(update) // 2] for update in bad_updates)
