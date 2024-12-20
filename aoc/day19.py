from functools import cache


def parse(lines):
    tokens = set(lines[0].split(", "))
    targets = lines[2:]
    return tokens, targets


def run(lines):
    tokens, targets = parse(lines)

    max_token = max(len(token) for token in tokens)

    @cache
    def count(s):
        """Return the count of possible ways to tokenize the input using a recursive algorithm.
        Consider increasingly large prefixes of the input (up to the maximum possible token size);
        if the prefix is a possible token, add the count of the input, less the prefix, to the count
        for this input.

        Example:
          Possible tokens: r, b, g, rb, gb, br
          Input: rrbgbr

          count(): base case
            -> 1
          count(r): "r" is possible token, so add count() = 1
            -> 1
          count(br): "b" is possible token, so add count(r) = 1
                     "br" is possible token, so add count() = 1
            -> 2
          count(gbr): "g" is possible token, so add count(br) = 2
                      "gb" is possible token, so add count(r) = 1
                      "gbr" is not possible token (and too long)
            -> 3
          count(bgbr): "b" is possible token, so add count(gbr) = 3
                       "bg" is not possible token
                       "bgb" is not possible token (and too long)
                       ...
            -> 3
          count(rbgbr): "r" is possible token, so add count(bgbr) = 3
                        "rb" is possible token, so add count(gbr) = 3
                        "rbg" is not possible token (and too long)
                        ...
            -> 6
          count(rrbgbr): "r" is possible token, so add count(rbgbr) = 6
                         "rr" is not possible token
                         "rrb" is not possible token (and too long)
                         ...
            -> 6

        So count(rrbgbr) = 6 corresponding to:
          r r b g b r
          r rb  g b r
          r r b gb  r
          r rb  gb  r
          r r b g br
          r rb  g br
        """
        if not s:
            return 1

        return sum(
            count(s[idx:]) for idx in range(1, min(max_token, len(s)) + 1) if s[:idx] in tokens
        )

    return [count(target) for target in targets]


def part1(lines):
    return sum(count > 0 for count in run(lines))


def part2(lines):
    return sum(run(lines))
