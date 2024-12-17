from dataclasses import dataclass
import re


@dataclass
class Registers:
    a: int
    b: int
    c: int

    def combo(self, operand) -> int:
        if operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c

        raise RuntimeError("Unknown combo operand")


def parse(data):
    a, b, c, *program = [int(x) for x in re.findall(r"\d+", data)]
    registers = Registers(a, b, c)
    return registers, program


def run(registers, program):
    size = len(program)
    ptr = 0
    output = list()

    while ptr < size:
        opcode, operand = program[ptr : ptr + 2]

        if opcode == 0:
            registers.a >>= registers.combo(operand)

        if opcode == 1:
            registers.b ^= operand

        if opcode == 2:
            registers.b = registers.combo(operand) & 7

        if opcode == 3:
            if registers.a:
                ptr = operand - 2  # will be incremented back to `operand` at the end of the loop

        if opcode == 4:
            registers.b ^= registers.c

        if opcode == 5:
            output.append(registers.combo(operand) & 7)

        if opcode == 6:
            registers.b = registers.a >> registers.combo(operand)

        if opcode == 7:
            registers.c = registers.a >> registers.combo(operand)

        ptr += 2

    return output


def part1(data):
    registers, program = parse(data)
    return ",".join(str(x) for x in run(registers, program))


def part2(data):
    _, program = parse(data)

    def options(prefix, target):
        """Return the 3-bit numbers which, when appended bitwise to the current number, would result
        in the target as the next output value (in reverse order).
        
        The rules were determined by manual inspection of the input program and are specific to my
        input program:

            2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0
        """

        # the 7 lowest bits of the current number determine the results here
        # let's represent the rules using the 7-bit representation: abcdefg
        # capital letter means its complement (bit flip)

        #                                             abcdefg
        # for example, consider the number 610 = 0x1001100010
        # the output when register A is initialized to 610 is 1,4,1,0
        #
        # appending 000 to this number gives us 0x1001100010000 = 4880
        # according to the rules below, 000 generates an additional output of fg1, or 0x101 = 5
        # the output when register A is initialized to 4880 is 5,1,4,1,0
        #
        # appending 101 to this number gives us 0x1001100010101 = 4885
        # according to the rules below, 101 generates an additional output of Abc, or 0x010 = 2
        # the output when register A is initialized to 4885 is 2,1,4,1,0

        # 000 -> fg1
        if (prefix & 3) << 1 | 1 == target:
            yield 0

        # 001 -> efg
        if prefix & 7 == target:
            yield 1

        # 010 -> 001
        if target == 1:
            yield 2

        # 011 -> g11
        if (prefix & 1) << 2 | 3 == target:
            yield 3

        # 100 -> BcD
        if prefix >> 3 & 7 ^ 5 == target:
            yield 4

        # 101 -> Abc
        if prefix >> 4 & 7 ^ 4 == target:
            yield 5

        # 110 -> DEF
        if prefix >> 1 & 7 ^ 7 == target:
            yield 6

        # 111 -> CDe
        if prefix >> 2 & 7 ^ 6 == target:
            yield 7

    # list which holds numbers for register A which output the program _so far_; start with 0
    candidates = [0]

    # for each output value, update the candidate list using the new possible 3-bit numbers
    for target in reversed(program):
        candidates = [c << 3 | option for c in candidates for option in options(c, target)]

    return min(candidates)
