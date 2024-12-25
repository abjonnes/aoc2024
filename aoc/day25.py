from itertools import product, takewhile
from typing import Generator


def part1(lines: list[list[str]]):
    def block_gen() -> Generator[list[list[str]], None, None]:
        it = iter(lines)
        while True:
            block = list(takewhile(bool, it))
            if not block:
                break
            yield block

    keys = list()
    locks = list()
    for block in block_gen():
        is_key = block[0] == "....."
        transpose = [[block[c][r] for c in range(7)] for r in range(5)]
        counts = [col.count("#") - 1 for col in transpose]
        if is_key:
            keys.append(counts)
        else:
            locks.append(counts)

    return sum(all(k + l <= 5 for k, l in zip(key, lock)) for key, lock in product(keys, locks))
