from collections import Counter


def parse(lines):
    list1 = list()
    list2 = list()
    for line in lines:
        a, b = line.split()
        list1.append(int(a))
        list2.append(int(b))

    return list1, list2


def part1(lines):
    list1, list2 = parse(lines)
    return sum(abs(a - b) for a, b in zip(sorted(list1), sorted(list2)))


def part2(lines):
    list1, list2 = parse(lines)
    counts = Counter(list2)
    return sum(x * counts[x] for x in list1)
