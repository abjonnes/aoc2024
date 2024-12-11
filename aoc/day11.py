from functools import cache
from math import floor, log10


def run(data, blinks):
    @cache
    def count(stone, n):
        if not n:
            return 1

        if stone == 0:
            return count(1, n - 1)

        n_digits = floor(log10(stone)) + 1
        
        if n_digits % 2 == 0:
            factor = 10 ** (n_digits / 2)
            return count(stone % factor, n - 1) + count(stone // factor, n - 1)

        return count(stone * 2024, n - 1)

    data = [int(x) for x in data.strip().split()]
    return sum(count(stone, blinks) for stone in data)


def part1(data):
    return run(data, 25)


def part2(data):
    return run(data, 75)
