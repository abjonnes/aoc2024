def parse(lines):
    for line in lines:
        yield [int(x) for x in line.split()]


def is_safe(data):
    diffs = [a - b for a, b in zip(data, data[1:])]
    return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)


def part1(lines):
    return sum(is_safe(entry) for entry in parse(lines))


def part2(lines):
    sum_ = 0
    for entry in parse(lines):
        for to_remove in range(len(entry)):
            new_entry = entry[:to_remove] + entry[to_remove + 1 :]
            if is_safe(new_entry):
                break
        else:  # loop was not broken, i.e. no subset was "safe"
            continue

        # we only get here if at least one subset was safe
        sum_ += 1

    return sum_
