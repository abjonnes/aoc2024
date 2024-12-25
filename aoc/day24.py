from functools import partial
import operator
from typing import Literal, overload

from blinker import Signal


class Gate:
    """Implement the gate connectivity using signals."""

    signal = Signal()  # a single signal instance for everything
    registry = list()  # keep track of all gates in existence

    def __init__(self, rep):
        self.input_a, op, self.input_b, _, self.output = rep.split()

        match op:
            case "AND":
                self.op = operator.and_
            case "OR":
                self.op = operator.or_
            case "XOR":
                self.op = operator.xor
            case _:
                raise ValueError(f"unrecognized gate operation: {op}")

        self.a_value = None
        self.b_value = None

        # listen to the two input channels and set/emit values accordingly
        self.signal.connect(self.receive_a, sender=self.input_a)
        self.signal.connect(self.receive_b, sender=self.input_b)

        self.registry.append(self)

    def receive_a(self, _, value):
        self.a_value = value
        self.check()

    def receive_b(self, _, value):
        self.b_value = value
        self.check()

    def check(self):
        """Emit a signal if both inputs have been set."""
        if not (self.a_value is None or self.b_value is None):
            self.signal.send(self.output, value=self.op(self.a_value, self.b_value))

    @classmethod
    def reset(cls):
        for gate in cls.registry:
            gate.a_value = gate.b_value = None


def parse(lines):
    lines = iter(lines)
    inputs = dict()
    for line in lines:
        if not line:
            break
        input_, value = line.split(": ")
        value = int(value)
        inputs[input_] = value

    gates = [Gate(line) for line in lines]

    return inputs, gates


def do_sum(inputs, gates):
    """Given inputs and gates, calculate the "sum" of the two binary integer input representation
    where the sum is a binary integer representation on the z__ gates.
    """
    n_z_gates = sum(gate.output.startswith("z") for gate in gates)

    # accumulator of the sum
    acc = 0

    # when a value is received on a z__ gate, incorporate it into the sum
    def collect(_, idx, value):
        nonlocal acc
        acc |= value << idx

    # define the partial functions here so that they don't get garbage collected when the call to
    # `connect` completes (signal.connect uses weak refs by default, and we'd like the connections
    # to expire when we leave `do_sum` so we can't use strong refs anyway)
    pfuncs = {idx: partial(collect, idx=idx) for idx in range(n_z_gates)}

    # connect the z__ gates
    for idx in range(n_z_gates):
        Gate.signal.connect(pfuncs[idx], sender=f"z{idx:02d}")

    # finally, provide the inputs; the sum will be populated into `acc` after all inputs are given
    for input_, value in inputs.items():
        Gate.signal.send(input_, value=value)

    # reset values for the next iteration
    Gate.reset()

    return acc


def part1(lines):
    inputs, gates = parse(lines)
    return do_sum(inputs, gates)


def part2(lines):
    """The machine is a series of "adders" which are circuits containing five gates (two gates for
    the first unit) which take two inputs (plus a carry input when present) and outputs a sum output
    plus a carry. Four individual adder units are broken due to two swapped outputs. Identify the
    four units, and then the outputs within each that are swapped.
    """
    inputs, gates = parse(lines)
    n_bits = len(inputs) // 2

    # first, identify the four defective adder units by sending a single "1" input bit into the
    # adder under consideration and inspecting the output
    bad_bits = list()
    inputs = {f"{v}{idx:02d}": 0 for v in ("x", "y") for idx in range(n_bits)}
    for bit in range(n_bits):
        override = {f"x{bit:02d}": 1}

        # if the sum is incorrect, the adder for this input bit is defective
        if do_sum(dict(inputs, **override), gates) != 1 << bit:
            bad_bits.append(bit)

    # if we've labeled more than four adders as defective, then the output swaps must not be
    # isolated to single adder units and the rest of our approach fails
    assert len(bad_bits) == 4, "swapped wires not isolated to individual adders"

    # fun with types
    @overload
    def find_gate(input_=..., output=..., op=..., check: Literal[True] = ...) -> Gate: ...

    @overload
    def find_gate(input_=..., output=..., op=..., check: Literal[False] = ...) -> Gate | None: ...

    def find_gate(input_=None, output=None, op=None, check=True):
        """Convenience method to find at most one gate which has the specified input, output or
        operation.
        """
        predicates = list()
        if input_:
            predicates.append(lambda g: input_ in (g.input_a, g.input_b))
        if output:
            predicates.append(lambda g: output == g.output)
        if op:
            predicates.append(lambda g: op is g.op)

        results = [g for g in gates if all(predicate(g) for predicate in predicates)]

        assert len(results) <= 1, "too many matching gates"

        if check:
            assert results, "no gates found"

        if results:
            return results[0]

    # collect all identified swaps
    bad_wires = set()

    # each correct adder (besides the first) is a "full" adder with 5 gates, where "x" and "y" are
    # the inputs from the user, "c" is the carry from the previous adder, "z" is the sum output, "C"
    # is the carry output, and "i", "j" and "k" are intermediate values:
    #
    # gate 1: x XOR y --> i
    # gate 2: c XOR i --> z  (output)
    # gate 3: x AND y --> j
    # gate 4: c AND i --> k
    # gate 5: j OR  k --> C  (output)
    #
    # in the dysfunctional adders, two of the outputs are swapped; here we try to identify them

    for bit in bad_bits:
        swap = set()

        # find the carry output (gate 5) from the previous adder by tracing from known inputs
        previous_gate_3 = find_gate(input_=f"x{bit-1}", op=operator.and_)
        previous_gate_5 = find_gate(input_=previous_gate_3.output, op=operator.or_)

        # we can positively identify these four gates in our adder right away because their inputs
        # are guaranteed to be correct
        gate_1 = find_gate(input_=f"x{bit}", op=operator.xor)
        gate_2 = find_gate(input_=previous_gate_5.output, op=operator.xor)
        gate_3 = find_gate(input_=f"x{bit}", op=operator.and_)
        gate_4 = find_gate(input_=previous_gate_5.output, op=operator.and_)

        # output of gate 1 should be an input to gate 4
        if gate_1.output not in (gate_4.input_a, gate_4.input_b):
            swap.add(gate_1.output)

        # output of gate 2 should be the sum output (z__)
        if gate_2.output != f"z{bit:02d}":
            swap.add(gate_2.output)

        # outputs of gates 3 and 4 should be the inputs to gate 5; we don't know gate 5 yet, so we
        # must attempt to locate it using either input
        gate_5a = find_gate(input_=gate_3.output, op=operator.or_, check=False)
        if not gate_5a:
            swap.add(gate_3.output)

        gate_5b = find_gate(input_=gate_4.output, op=operator.or_, check=False)
        if not gate_5b:
            swap.add(gate_4.output)

        # if we've only identified one swapped output among gates 1-4 by this point, then gate 5's
        # output must be swapped
        if len(swap) == 1:
            # we must have located gate 5 using either gate 3 or gate 4's output, since at least one
            # of those outputs is correct
            gate_5 = gate_5a or gate_5b
            assert gate_5
            swap.add(gate_5.output)

        bad_wires.update(swap)

    return ",".join(sorted(bad_wires))
