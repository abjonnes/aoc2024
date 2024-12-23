from collections import defaultdict
from itertools import combinations, filterfalse
import sys

# support deeper recursion for graph algorithms
sys.setrecursionlimit(2000)


def parse(lines):
    """Parse and return the adjacency matrix for the graph."""
    adj = defaultdict(set)

    for line in lines:
        n1, n2 = line.split("-")
        adj[n1].add(n2)
        adj[n2].add(n1)

    return adj


def part1(lines):
    adj = parse(lines)

    # observed 3-cliques having at least one node which starts with "t"
    seen = set()

    for node, neighbors in adj.items():
        if not node.startswith("t"):
            continue

        # consider every pair of nodes connected to this node; if the pair are also connected, we've
        # found a 3-clique
        for a, b in combinations(neighbors, r=2):
            # frozensets are hashable and so can themselves be set elements
            s = frozenset((node, a, b))

            if a in adj[b] and s not in seen:
                seen.add(s)

    return len(seen)


def part2(lines):
    adj = parse(lines)

    def uniqify(func):
        """Decorator which ensures only unique elements are yielded from a generator."""

        def decorator(*args, **kwargs):
            seen = set()
            for x in filterfalse(seen.__contains__, func(*args, **kwargs)):
                seen.add(x)
                yield x

        return decorator

    @uniqify
    def maximal_cliques(g):
        """Yield maximal cliques in the graph using a recursive algorithm."""
        # base case
        if not g:
            yield frozenset()
            return

        # consider the subgraph of g after removing an arbitrary node v
        v = g.pop()

        # for every maximal clique of the subgraph, we can generate two possibly non-unique maximal
        # cliques in g
        for sub in maximal_cliques(g):
            # if adding v to a maximal clique of the subgraph results in a clique in g, that
            # resulting clique is by definition a maximal clique of g; otherwise, the subgraph's
            # maximal clique is itself a maximal clique of g
            if sub <= adj[v]:  # if adding v would result in a clique
                sub |= {v}
            yield sub

            # adding v to and removing non-neighbors of v from the maximal clique of the subgraph is
            # a maximal clique of g (the same as the one we just yielded, if the condition above was
            # true)
            sub &= adj[v]
            sub |= {v}
            yield sub

    return ",".join(sorted(max(maximal_cliques(set(adj)), key=len)))
