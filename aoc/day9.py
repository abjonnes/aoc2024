from dataclasses import dataclass
from functools import total_ordering
from itertools import accumulate, chain, repeat, zip_longest


def part1(data):
    data = [int(x) for x in data.strip()]

    # assert that free space indicators exist only between file indicators
    assert len(data) % 2 == 1

    n_files = len(data) // 2 + 1
    total_block_size = sum(data[::2])

    # create an iterator which yields labeled file blocks and blanks from left to right from the
    # original orientation; blanks are represented by `None`s
    forward_generators = chain.from_iterable(
        (repeat(file_idx, a), repeat(None, b or 0))
        for file_idx, (a, b) in enumerate(zip_longest(data[::2], data[1::2]))
    )
    forward_it = chain.from_iterable(forward_generators)

    # create an iterator which file labeled blocks (only) from _right to left_ from the original
    # orientation
    reverse_generators = chain(
        repeat(n_files - file_idx - 1, x) for file_idx, x in enumerate(data[::-2])
    )
    reverse_it = chain.from_iterable(reverse_generators)

    def next_block():
        """Return the next file block from the forward iterator, or the reverse iterator if we hit a
        blank.
        """
        block = next(forward_it)
        if block is None:
            block = next(reverse_it)

        return block

    return sum(block_idx * next_block() for block_idx in range(total_block_size))


def part2(data):
    data = [int(x) for x in data.strip()]

    @total_ordering
    @dataclass
    class Block:
        start: int
        length: int
        label: int | None = None

        def __lt__(self, other):
            return self.start < other.start

        @property
        def end(self):
            return self.start + self.length

    # assert that free space indicators exist only between file indicators
    assert len(data) % 2 == 1

    # list of locations of initial file starts
    file_starts = [0]
    file_starts.extend(accumulate(data))

    files = [
        Block(file_pos, file_len, file_idx)
        for file_idx, (file_len, file_pos) in enumerate(zip(data[::2], file_starts[::2]))
    ]

    blanks = [
        Block(blank_pos, blank_len)
        for blank_pos, blank_len in zip(file_starts[1::2], data[1::2])
        if blank_len  # ignore empty blank spaces (i.e. no blank)
    ]

    file_map = {file.label: file for file in files}

    for file_idx in reversed(range(len(files))):
        file = file_map[file_idx]
        try:
            blank = next(
                blank
                for blank in blanks
                if blank.start < file.start and blank.length >= file.length
            )
        except StopIteration:
            continue

        # create a new blank where the file was
        new_blank = Block(file.start, file.length)

        # move file to where the blank was
        file.start = blank.start
        files.sort()

        # shrink old blank and remove it if it's completely occupied now
        blank.start += file.length
        blank.length -= file.length
        if not blank.length:
            blanks.remove(blank)

        # attempt to merge new blank with adjacent blanks
        try:
            left_blank = next(blank for blank in blanks if blank.end == new_blank.start)
            new_blank.start = left_blank.start
            new_blank.length += left_blank.length
            blanks.remove(left_blank)
        except StopIteration:
            pass

        try:
            right_blank = next(blank for blank in blanks if blank.start == new_blank.end)
            new_blank.length += right_blank.length
            blanks.remove(right_blank)
        except StopIteration:
            pass

        blanks.append(new_blank)
        blanks.sort()

    return sum(file.label * x for file in files for x in range(file.start, file.end))
