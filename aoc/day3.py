import re

# group 1: "do" if present
# group 2: "don't" if present
# group 3: "mul" if present
# group 4: first number of `mul` if present
# group 5: second number of `mul` if present
PATTERN = re.compile(r"(do)\(\)|(don't)\(\)|(mul)\((\d{1,3}),(\d{1,3})\)")


def part1(data):
    return sum(int(m.group(4)) * int(m.group(5)) for m in PATTERN.finditer(data) if m.group(3))


def part2(data):
    on = True
    sum_ = 0
    for m in PATTERN.finditer(data):
        if m.group(1):
            on = True
            continue
        if m.group(2):
            on = False
            continue
        if m.group(3) and on:
            sum_ += int(m.group(4)) * int(m.group(5))

    return sum_
