from collections import defaultdict, deque


def calculate(num):
    num = num ^ (num * 64) % 16777216
    num = num ^ (num // 32) % 16777216
    num = num ^ (num * 2048) % 16777216
    return num


def part1(lines):
    def run(lines):
        for line in lines:
            num = int(line)
            for _ in range(2000):
                num = calculate(num)
            yield num

    return sum(run(lines))


def part2(lines):
    bananas = defaultdict(int)

    def run(num):
        """For each monkey's observed price change sequences, note how many bananas would be
        acquired.
        """
        # additional elements get discarded from the opposite side of the deque
        q = deque(maxlen=4)

        # keep track of observed sequences since only the first observation counts
        seen = set()

        value = num % 10
        for _ in range(2000):
            num = calculate(num)
            new_value = num % 10

            # note the new price difference
            q.append(new_value - value)

            value = new_value

            # the most recent sequence of price changes, up to 4
            curr_seq = tuple(q)

            if curr_seq in seen or len(curr_seq) < 4:
                continue

            bananas[curr_seq] += value
            seen.add(curr_seq)

    for line in lines:
        run(int(line))

    return max(bananas.values())
